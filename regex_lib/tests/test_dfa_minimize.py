import unittest
from automata import DFA
from dfa_minimize import minimize_dfa


class TestDfaMinimize(unittest.TestCase):
    def test_minimize_simple(self):
        # DFA with redundant states
        dfa = DFA({0, 1, 2}, {0: {"a": 1}, 1: {"a": 2}, 2: {"a": 2}}, 0, {2})
        min_dfa = minimize_dfa(dfa)
        self.assertLessEqual(len(min_dfa.states), len(dfa.states))


if __name__ == "__main__":
    unittest.main()
