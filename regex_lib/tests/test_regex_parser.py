import unittest
from regex_parser import RegexParser, Literal, Concat, Alternation, Star


class TestRegexParser(unittest.TestCase):
    def test_literal(self):
        parser = RegexParser("a")
        ast = parser.parse()
        self.assertIsInstance(ast, Literal)
        self.assertEqual(ast.char, "a")

    def test_concat(self):
        parser = RegexParser("ab")
        ast = parser.parse()
        self.assertIsInstance(ast, Concat)
        self.assertIsInstance(ast.left, Literal)
        self.assertEqual(ast.left.char, "a")
        self.assertIsInstance(ast.right, Literal)
        self.assertEqual(ast.right.char, "b")

    def test_alternation(self):
        parser = RegexParser("a|b")
        ast = parser.parse()
        self.assertIsInstance(ast, Alternation)
        self.assertIsInstance(ast.left, Literal)
        self.assertEqual(ast.left.char, "a")
        self.assertIsInstance(ast.right, Literal)
        self.assertEqual(ast.right.char, "b")

    def test_star(self):
        parser = RegexParser("a*")
        ast = parser.parse()
        self.assertIsInstance(ast, Star)
        self.assertIsInstance(ast.expr, Literal)
        self.assertEqual(ast.expr.char, "a")

    def test_parentheses(self):
        parser = RegexParser("(a|b)*")
        ast = parser.parse()
        self.assertIsInstance(ast, Star)
        self.assertIsInstance(ast.expr, Alternation)


if __name__ == "__main__":
    unittest.main()
