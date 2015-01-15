from nfa import NFA


def epsilon():
    return NFA(
        num_states=1,
        start_state=0,
        end_states=[0],
        transitions={})


def character(c):
    return NFA(
        num_states=2,
        start_state=0,
        end_states=[1],
        transitions={
            0: [(c, 1)]
        })


def concat(r1, r2):
    offset = r1.num_states
    r2 = r2.Offset(offset)

    trans = {}
    trans.update(r1.transitions)
    trans.update(r2.transitions)

    for es in r1.end_states:
        if es in trans:
            trans[es].append((None, r2.start_state))
        else:
            trans[es] = [(None, r2.start_state)]

    return NFA(
        num_states=r1.num_states + r2.num_states,
        start_state=r1.start_state,
        end_states=r2.end_states,
        transitions=trans)
