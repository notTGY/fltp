from collections import deque
from automata import DFA


def epsilon_closure(nfa, states):
    closure = set(states)
    queue = deque(states)
    while queue:
        state = queue.popleft()
        if "" in nfa.transitions.get(state, {}):
            for next_state in nfa.transitions[state][""]:
                if next_state not in closure:
                    closure.add(next_state)
                    queue.append(next_state)
    return frozenset(closure)


def move(nfa, states, symbol):
    result = set()
    for state in states:
        if symbol in nfa.transitions.get(state, {}):
            result.update(nfa.transitions[state][symbol])
    return result


def nfa_to_dfa(nfa):
    start_closure = epsilon_closure(nfa, {nfa.start})
    dfa_states = {start_closure}
    dfa_transitions = {}
    unmarked = [start_closure]
    state_map = {start_closure: 0}  # map frozenset to DFA state id
    state_counter = 1

    while unmarked:
        current = unmarked.pop()
        dfa_transitions[state_map[current]] = {}
        symbols = set()
        for s in current:
            symbols.update(nfa.transitions.get(s, {}).keys())
        symbols.discard("")  # remove epsilon
        for symbol in symbols:
            move_states = move(nfa, current, symbol)
            if move_states:
                closure = epsilon_closure(nfa, move_states)
                if closure not in dfa_states:
                    dfa_states.add(closure)
                    state_map[closure] = state_counter
                    state_counter += 1
                    unmarked.append(closure)
                dfa_transitions[state_map[current]][symbol] = state_map[closure]

    dfa_accept = {state_map[s] for s in dfa_states if any(ns in nfa.accept for ns in s)}

    return DFA(set(range(len(dfa_states))), dfa_transitions, 0, dfa_accept)
