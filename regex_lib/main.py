import sys
from regex_parser import RegexParser
from thompson import Thompson
from nfa_to_dfa import nfa_to_dfa
from dfa_minimize import minimize_dfa
from json_output import nfa_to_json, dfa_to_json

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <regex>")
        sys.exit(1)

    regex = sys.argv[1]
    parser = RegexParser(regex)
    ast = parser.parse()

    thompson = Thompson()
    nfa = thompson.build_nfa(ast)

    print("NFA:")
    print(nfa_to_json(nfa))

    dfa = nfa_to_dfa(nfa)

    print("DFA:")
    print(dfa_to_json(dfa))

    min_dfa = minimize_dfa(dfa)

    print("Minimized DFA:")
    print(dfa_to_json(min_dfa))
