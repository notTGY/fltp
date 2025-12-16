import unittest
from regex_parser import RegexParser
from thompson import Thompson


class TestThompson(unittest.TestCase):
    def test_literal(self):
        parser = RegexParser("a")
        ast = parser.parse()
        thompson = Thompson()
        nfa = thompson.build_nfa(ast)
        self.assertEqual(len(nfa.states), 2)
        self.assertEqual(nfa.start, 0)
        self.assertEqual(nfa.accept, {1})
        self.assertIn(0, nfa.transitions)
        self.assertIn("a", nfa.transitions[0])
        self.assertEqual(nfa.transitions[0]["a"], [1])

    def test_concat(self):
        parser = RegexParser("ab")
        ast = parser.parse()
        thompson = Thompson()
        nfa = thompson.build_nfa(ast)
        # check states and transitions
        self.assertGreater(len(nfa.states), 2)

    def test_alternation(self):
        parser = RegexParser("a|b")
        ast = parser.parse()
        thompson = Thompson()
        nfa = thompson.build_nfa(ast)
        self.assertGreater(len(nfa.states), 2)

    def test_star(self):
        parser = RegexParser("a*")
        ast = parser.parse()
        thompson = Thompson()
        nfa = thompson.build_nfa(ast)
        self.assertGreater(len(nfa.states), 2)


if __name__ == "__main__":
    unittest.main()
