from automata import DFA


def minimize_dfa(dfa):
    states = list(dfa.states)
    n = len(states)
    # create table: list of lists, True if distinguishable
    table = [[False for _ in range(n)] for _ in range(n)]

    # mark accepting vs non-accepting
    for i in range(n):
        for j in range(i + 1, n):
            if (states[i] in dfa.accept) != (states[j] in dfa.accept):
                table[i][j] = True

    # iteratively mark
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                if not table[i][j]:
                    # check if distinguishable via some transition
                    for symbol, trans in dfa.transitions[states[i]].items():
                        next_i = trans
                        next_j = dfa.transitions[states[j]].get(symbol)
                        if (
                            next_j is None
                            or table[min(next_i, next_j)][max(next_i, next_j)]
                        ):
                            table[i][j] = True
                            changed = True
                            break

    # now, merge states that are not distinguishable
    # use union-find or just group
    groups = []
    visited = [False] * n
    for i in range(n):
        if not visited[i]:
            group = [states[i]]
            for j in range(i + 1, n):
                if not table[i][j]:
                    group.append(states[j])
                    visited[j] = True
            groups.append(group)

    # create new DFA
    new_states = list(range(len(groups)))
    state_map = {}
    for idx, group in enumerate(groups):
        for s in group:
            state_map[s] = idx

    new_transitions = {}
    for idx, group in enumerate(groups):
        new_transitions[idx] = {}
        # use the first state in group for transitions
        rep = group[0]
        for symbol, next_s in dfa.transitions[rep].items():
            new_transitions[idx][symbol] = state_map[next_s]

    new_start = state_map[dfa.start]
    new_accept = {state_map[s] for s in dfa.accept}

    return DFA(set(new_states), new_transitions, new_start, new_accept)
