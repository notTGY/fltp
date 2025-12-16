from regex_parser import RegexNode, Literal, Concat, Alternation, Star
from automata import NFA


class Thompson:
    def __init__(self):
        self.state_counter = 0

    def new_state(self):
        self.state_counter += 1
        return self.state_counter - 1

    def build_nfa(self, regex):
        return self._build(regex)

    def _build(self, node):
        if isinstance(node, Literal):
            start = self.new_state()
            accept = self.new_state()
            transitions = {start: {node.char: [accept]}}
            return NFA({start, accept}, transitions, start, {accept})
        elif isinstance(node, Concat):
            left_nfa = self._build(node.left)
            right_nfa = self._build(node.right)
            # add epsilon transition from left accept to right start
            acc = next(iter(left_nfa.accept))
            left_nfa.transitions[acc].setdefault("", []).append(right_nfa.start)
            left_nfa.transitions.update(right_nfa.transitions)
            left_nfa.states.update(right_nfa.states)
            left_nfa.accept = right_nfa.accept
            return left_nfa
        elif isinstance(node, Alternation):
            left_nfa = self._build(node.left)
            right_nfa = self._build(node.right)
            start = self.new_state()
            accept = self.new_state()
            transitions = {start: {"": [left_nfa.start, right_nfa.start]}}
            transitions.update(left_nfa.transitions)
            transitions.update(right_nfa.transitions)
            for acc in left_nfa.accept | right_nfa.accept:
                transitions.setdefault(acc, {}).setdefault("", []).append(accept)
            states = {start, accept} | left_nfa.states | right_nfa.states
            return NFA(states, transitions, start, {accept})
        elif isinstance(node, Star):
            expr_nfa = self._build(node.expr)
            start = self.new_state()
            accept = self.new_state()
            transitions = {start: {"": [expr_nfa.start, accept]}}
            for acc in expr_nfa.accept:
                transitions.setdefault(acc, {}).setdefault("", []).append(
                    expr_nfa.start
                )
                transitions.setdefault(acc, {}).setdefault("", []).append(accept)
            transitions.update(expr_nfa.transitions)
            states = {start, accept} | expr_nfa.states
            return NFA(states, transitions, start, {accept})
        elif isinstance(node, Star):
            expr_nfa = self._build(node.expr)
            start = self.new_state()
            accept = self.new_state()
            transitions = {start: {"": [expr_nfa.start, accept]}}
            for acc in expr_nfa.accept:
                expr_nfa.transitions[acc].setdefault("", []).append(expr_nfa.start)
                expr_nfa.transitions[acc].setdefault("", []).append(accept)
            transitions.update(expr_nfa.transitions)
            states = {start, accept} | expr_nfa.states
            return NFA(states, transitions, start, {accept})
