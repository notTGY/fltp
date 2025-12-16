import argparse
import json
import sys
from regex_parser import RegexParser
from thompson import Thompson
from nfa_to_dfa import nfa_to_dfa
from dfa_minimize import minimize_dfa
from json_output import nfa_to_json, dfa_to_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert regex to automata")
    parser.add_argument("regex", help="Regular expression string")
    parser.add_argument("--nfa", action="store_true", help="Output only NFA")
    parser.add_argument("--dfa", action="store_true", help="Output NFA and DFA")
    parser.add_argument(
        "--verbose", action="store_true", help="Print labels for each automaton"
    )
    parser.add_argument("--ast", action="store_true", help="Print AST")

    args = parser.parse_args()

    regex_parser = RegexParser(args.regex)
    ast = regex_parser.parse()

    if args.ast:
        print(ast)
        sys.exit(0)

    thompson = Thompson()
    nfa = thompson.build_nfa(ast)

    nfa_json = nfa_to_json(nfa)
    if args.verbose:
        print("NFA:")
        print(nfa_json)

    if args.nfa:
        if not args.verbose:
            print(nfa_json)
        sys.exit(0)

    dfa = nfa_to_dfa(nfa)
    dfa_json = dfa_to_json(dfa)
    if args.verbose:
        print("DFA:")
        print(dfa_json)

    if args.dfa:
        if not args.verbose:
            print(dfa_json)
        sys.exit(0)

    min_dfa = minimize_dfa(dfa)
    min_dfa_json = dfa_to_json(min_dfa)
    if args.verbose:
        print("Minimized DFA:")
    print(min_dfa_json)
