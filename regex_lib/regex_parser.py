class RegexNode:
    pass


class Literal(RegexNode):
    def __init__(self, char):
        self.char = char


class Concat(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Alternation(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Star(RegexNode):
    def __init__(self, expr):
        self.expr = expr


class RegexParser:
    def __init__(self, regex):
        self.regex = regex
        self.pos = 0

    def parse(self):
        return self._parse_expr()

    def _parse_expr(self):
        left = self._parse_term()
        while self.pos < len(self.regex) and self.regex[self.pos] == "|":
            self.pos += 1
            right = self._parse_term()
            left = Alternation(left, right)
        return left

    def _parse_term(self):
        left = self._parse_factor()
        while self.pos < len(self.regex) and self.regex[self.pos] not in "|)*":
            right = self._parse_factor()
            left = Concat(left, right)
        return left

    def _parse_factor(self):
        if self.regex[self.pos] == "(":
            self.pos += 1
            expr = self._parse_expr()
            if self.regex[self.pos] != ")":
                raise ValueError("Mismatched parentheses")
            self.pos += 1
        else:
            expr = Literal(self.regex[self.pos])
            self.pos += 1
        if self.pos < len(self.regex) and self.regex[self.pos] == "*":
            self.pos += 1
            expr = Star(expr)
        return expr
