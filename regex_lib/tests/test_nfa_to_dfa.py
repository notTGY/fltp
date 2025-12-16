import unittest
from automata import NFA
from nfa_to_dfa import nfa_to_dfa


class TestNfaToDfa(unittest.TestCase):
    def test_simple_nfa(self):
        # NFA for 'a'
        nfa = NFA({0, 1}, {0: {"a": [1]}}, 0, {1})
        dfa = nfa_to_dfa(nfa)
        self.assertEqual(len(dfa.states), 2)
        self.assertEqual(dfa.start, 0)
        self.assertEqual(dfa.accept, {1})

    def test_nfa_with_epsilon(self):
        # NFA with epsilon
        nfa = NFA({0, 1, 2}, {0: {"": [1]}, 1: {"a": [2]}}, 0, {2})
        dfa = nfa_to_dfa(nfa)
        self.assertGreater(len(dfa.states), 1)


if __name__ == "__main__":
    unittest.main()
