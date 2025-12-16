# Regex Library

This is a Python3 library for processing regular expressions, converting them into finite automata (NFA and DFA), minimizing the DFA, and outputting the results in JSON format. It implements the full pipeline from regex string to optimized DFA without using any external libraries.

## Features

- **Regex Parsing**: Converts a regex string into an Abstract Syntax Tree (AST) supporting:
  - Literals (e.g., `a`, `b`)
  - Concatenation (e.g., `ab`)
  - Alternation (e.g., `a|b`)
  - Kleene star (e.g., `a*`)
  - Parentheses for grouping (e.g., `(a|b)*`)

- **Thompson's Construction**: Builds a Non-Deterministic Finite Automaton (NFA) from the regex AST.

- **Subset Construction**: Converts the NFA to a Deterministic Finite Automaton (DFA) using epsilon-closure and move operations.

- **DFA Minimization**: Reduces the DFA to its minimal form using the table-filling algorithm.

- **JSON Output**: Exports NFA and DFA structures to JSON for visualization or further processing.

## Algorithms Overview

### Regex Parsing
The parser uses a recursive descent approach to build an AST from the regex string. It handles operator precedence: star has highest precedence, then concatenation, then alternation. Parentheses override precedence.

For example, `a|b*` is parsed as alternation of `a` and `b*`.

### Thompson's Construction
This algorithm builds an NFA from the regex AST by composing smaller NFAs for each subexpression. Each construct has a specific NFA pattern:

- **Literal** (`a`): Two states with a transition on `a`.
- **Concatenation** (`ab`): Connect the accept state of the first NFA to the start of the second via epsilon.
- **Alternation** (`a|b`): New start state with epsilon to both sub-NFAs, and epsilon from their accepts to a new accept.
- **Star** (`a*`): New start and accept, with epsilon loops back to the sub-NFA.

Epsilon transitions allow non-deterministic choices, enabling the NFA to match the regex.

### Subset Construction (NFA to DFA)
To make the automaton deterministic, we use subset construction:

1. Start with the epsilon-closure of the NFA's start state as the initial DFA state.
2. For each DFA state (a set of NFA states), compute transitions on each symbol by:
   - Finding NFA states reachable on that symbol.
   - Taking their epsilon-closure.
3. Repeat until no new states are added.
4. A DFA state is accepting if it contains any NFA accepting state.

This eliminates epsilon transitions and non-determinism.

### DFA Minimization
The table-filling algorithm minimizes the DFA by merging equivalent states:

1. Create a table marking pairs of states as distinguishable.
2. Initially mark pairs where one is accepting and one is not.
3. Iteratively mark pairs where transitions lead to already marked pairs.
4. Unmarked pairs are equivalent and can be merged.
5. Rebuild the DFA with merged states.

This reduces the number of states while preserving language acceptance.

## Usage

### Command Line
Run the full pipeline with:
```bash
python3 main.py "regex"
```
Example:
```bash
python3 main.py "a|b"
```
Outputs NFA, DFA, and minimized DFA in JSON.

### Makefile
- `make test`: Run all unit tests.
- `make run`: Run with default regex `'a|b'`.
- `make run REGEX='your_regex'`: Run with custom regex.

## Project Structure

- `automata.py`: NFA and DFA class definitions.
- `regex_parser.py`: Regex string to AST parser.
- `thompson.py`: Thompson's construction for NFA building.
- `nfa_to_dfa.py`: Subset construction for DFA conversion.
- `dfa_minimize.py`: DFA minimization algorithm.
- `json_output.py`: JSON serialization for automata.
- `main.py`: Command-line interface for the full pipeline.
- `tests/`: Unit tests for each module.
- `Makefile`: Build commands.

## Testing
Run tests with:
```bash
make test
```
Or directly:
```bash
python3 -m unittest discover -s tests
```

All tests pass, covering parsing, NFA construction, DFA conversion, minimization, and JSON output.