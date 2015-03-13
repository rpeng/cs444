import collections
from structs.dfa import DFA


def NFAToDFA(nfa):
    counter = 0
    new_states = {}
    start_state = frozenset(nfa.EpsilonClosure([nfa.start_state]))
    end_states = []

    transitions = collections.defaultdict(dict)

    work_list = []
    work_list.append(start_state)

    while work_list:
        states = work_list.pop()
        if states in new_states:
            continue

        new_states[states] = counter
        if states & nfa.end_states:
            end_states.append(counter)
        counter += 1

        temp_transitions = collections.defaultdict(set)
        for state in states:
            if state not in nfa.transitions:
                continue
            for token, next in nfa.transitions[state]:
                if token is not None:
                    temp_transitions[token] |= nfa.EpsilonClosure([next])

        for token, next_states in temp_transitions.items():
            next_states = frozenset(next_states)
            if token not in transitions[states]:
                transitions[states][token] = next_states
            if next_states not in new_states:
                work_list.append(next_states)

    # Convert back to numbers, populate end states
    numbered_transitions = collections.defaultdict(dict)
    for prev_state, input_map in transitions.items():
        for token, next_state in input_map.items():
            prev_idx = new_states[prev_state]
            next_idx = new_states[next_state]
            numbered_transitions[prev_idx][token] = next_idx

    return DFA(num_states=counter,
               start_state=new_states[start_state],
               end_states=end_states,
               transitions=numbered_transitions)
