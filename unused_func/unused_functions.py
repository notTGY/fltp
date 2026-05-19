from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path


@dataclass
class FunctionInfo:
    name: str
    line: int | None
    node: dict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find functions reachable from main in a .c file using clang AST."
    )
    parser.add_argument("source", help="Path to a .c file")
    parser.add_argument(
        "--clang",
        default="clang",
        help="clang executable to use (default: clang)",
    )
    parser.add_argument(
        "--clang-arg",
        action="append",
        default=[],
        help="Extra argument passed to clang. Can be used multiple times.",
    )
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_ast(source: Path, clang: str, clang_args: list[str]) -> dict:
    command = [
        clang,
        *clang_args,
        "-Xclang",
        "-ast-dump=json",
        "-fsyntax-only",
        str(source),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        fail(
            result.stderr.strip() or f"clang failed with exit code {result.returncode}"
        )

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"failed to parse clang AST as JSON: {exc}")


def is_source_function(node: dict, source: Path) -> bool:
    source = source.resolve()
    locations = [node.get("loc", {}), node.get("range", {}).get("begin", {})]

    for location in locations:
        if not isinstance(location, dict):
            continue
        if "includedFrom" in location:
            return False

        explicit_file = location.get("expansionLoc", {}).get("file") or location.get(
            "file"
        )
        if explicit_file and Path(explicit_file).resolve() != source:
            return False

    return True


def function_body(node: dict) -> dict | None:
    for child in node.get("inner", []):
        if child.get("kind") == "CompoundStmt":
            return child
    return None


def collect_function_definitions(ast: dict, source: Path) -> dict[str, FunctionInfo]:
    functions: dict[str, FunctionInfo] = {}

    for node in ast.get("inner", []):
        if node.get("kind") != "FunctionDecl":
            continue
        if not is_source_function(node, source):
            continue

        body = function_body(node)
        if body is None:
            continue

        name = node.get("name")
        if not name:
            continue

        line = node.get("loc", {}).get("line") or node.get("range", {}).get(
            "begin", {}
        ).get("line")
        functions[name] = FunctionInfo(name=name, line=line, node=node)

    return functions


def walk_inner(node: dict):
    yield node
    for child in node.get("inner", []):
        yield from walk_inner(child)


def direct_callee_name(call_expr: dict) -> str | None:
    inner = call_expr.get("inner", [])
    if not inner:
        return None

    callee_expr = inner[0]
    for node in walk_inner(callee_expr):
        if node.get("kind") != "DeclRefExpr":
            continue

        referenced_decl = node.get("referencedDecl", {})
        if referenced_decl.get("kind") == "FunctionDecl":
            return referenced_decl.get("name")

    return None


def build_call_graph(functions: dict[str, FunctionInfo]) -> dict[str, list[str]]:
    graph: dict[str, set[str]] = {name: set() for name in functions}

    for name, function in functions.items():
        for node in walk_inner(function.node):
            if node.get("kind") != "CallExpr":
                continue

            callee = direct_callee_name(node)
            if callee in functions:
                graph[name].add(callee)

    return {name: sorted(callees) for name, callees in graph.items()}


def reachable_from_main(graph: dict[str, list[str]]) -> tuple[set[str], list[str]]:
    seen: set[str] = set()
    order: list[str] = []
    queue: deque[str] = deque(["main"])

    while queue:
        current = queue.popleft()
        if current in seen:
            continue

        seen.add(current)
        order.append(current)
        queue.extend(graph.get(current, []))

    return seen, order


def ordered_names(
    names: set[str] | list[str], functions: dict[str, FunctionInfo]
) -> list[str]:
    return sorted(
        names,
        key=lambda name: (name != "main", functions[name].line or sys.maxsize, name),
    )


def print_function(name: str, functions: dict[str, FunctionInfo]) -> str:
    print(f"{functions[name].line}:{name}" if functions[name].line is not None else name)


def main() -> None:
    args = parse_args()

    source = Path(args.source)
    if source.suffix != ".c":
        fail("the input file must have the .c extension")
    if not source.is_file():
        fail(f"file not found: {source}")

    ast = load_ast(source, args.clang, args.clang_arg)
    functions = collect_function_definitions(ast, source)

    if "main" not in functions:
        fail("no main function definition found in the source file")

    graph = build_call_graph(functions)
    reachable, reachable_order = reachable_from_main(graph)
    unreachable = set(functions) - reachable

    print(f"Functions defined in file: {len(functions)}")
    print()
    print("Reachable from main:")
    for name in reachable_order:
        print_function(name, functions)

    print()
    print("Unreachable from main:")
    if unreachable:
        for name in ordered_names(unreachable, functions):
            print_function(name, functions)
        raise SystemExit(1)
    else:
        print("- none")


if __name__ == "__main__":
    main()
