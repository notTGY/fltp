class NFA:
    def __init__(self, states, transitions, start, accept):
        self.states = states  # set of states
        self.transitions = transitions  # dict: state -> dict: symbol -> list of states
        for state in states:
            self.transitions.setdefault(state, {})
        self.start = start
        self.accept = accept  # set of accept states


class DFA:
    def __init__(self, states, transitions, start, accept):
        self.states = states  # set of states
        self.transitions = transitions  # dict: state -> dict: symbol -> state
        for state in states:
            self.transitions.setdefault(state, {})
        self.start = start
        self.accept = accept  # set of accept states
