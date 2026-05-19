# unused_func

Small homework solution for the task:

1. Take a `.c` file.
2. Build its AST with `clang`.
3. Read the AST into memory.
4. Traverse it and find which functions are reachable from `main`.

## Requirements

- `python3`
- `clang`

## Usage

```bash
python3 unused_functions.py sample.c
```

To print the direct call graph too:

```bash
python3 unused_functions.py sample.c --show-calls
```

If your C file needs extra compiler flags, pass them through to `clang`:

```bash
python3 unused_functions.py program.c --clang-arg=-std=c11 --clang-arg=-Iinclude
```

## Notes

- The script only accepts files with the `.c` extension.
- The script reports functions defined in the input file itself.
- Direct function calls are resolved from the AST.
- Calls through function pointers are not mapped to a concrete target function.
