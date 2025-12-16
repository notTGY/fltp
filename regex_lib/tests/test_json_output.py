import unittest
import json
from automata import NFA, DFA
from json_output import nfa_to_json, dfa_to_json


class TestJsonOutput(unittest.TestCase):
    def test_nfa_to_json(self):
        nfa = NFA({0, 1}, {0: {"a": [1]}}, 0, {1})
        json_str = nfa_to_json(nfa)
        data = json.loads(json_str)
        self.assertIn("states", data)
        self.assertIn("transitions", data)

    def test_dfa_to_json(self):
        dfa = DFA({0, 1}, {0: {"a": 1}}, 0, {1})
        json_str = dfa_to_json(dfa)
        data = json.loads(json_str)
        self.assertIn("states", data)
        self.assertIn("transitions", data)


if __name__ == "__main__":
    unittest.main()
