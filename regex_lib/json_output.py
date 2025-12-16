import json


def nfa_to_json(nfa):
    data = {
        "states": sorted(list(nfa.states)),
        "transitions": nfa.transitions,
        "start": nfa.start,
        "accept": sorted(list(nfa.accept)),
    }
    return json.dumps(data, indent=2)


def dfa_to_json(dfa):
    data = {
        "states": sorted(list(dfa.states)),
        "transitions": dfa.transitions,
        "start": dfa.start,
        "accept": sorted(list(dfa.accept)),
    }
    return json.dumps(data, indent=2)
