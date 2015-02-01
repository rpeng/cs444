from nfa import NFA


def Concat(r1, r2):
    r2 = r2.Offset(r1.num_states)

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


def ConcatsOf(*regs):
    result = epsilon
    for reg in regs:
        result = Concat(result, reg)
    return result


def Optional(re):
    return Union(re, epsilon)


def OneOrMore(re):
    return Concat(re, ZeroOrMore(re))


def ZeroOrMore(re):
    re = re.Offset(1)
    trans = {}
    trans.update(re.transitions)
    trans[0] = [(None, re.start_state)]
    for es in re.end_states:
        if es in trans:
            trans[es].append((None, 0))
        else:
            trans[es] = [(None, 0)]

    return NFA(
        num_states=re.num_states + 1,
        start_state=0,
        end_states=list(re.end_states)+[0],
        transitions=trans
    )


def Union(r1, r2):
    r1 = r1.Offset(1)
    r2 = r2.Offset(1 + r1.num_states)

    trans = {}
    trans.update(r1.transitions)
    trans.update(r2.transitions)
    trans[0] = [(None, r1.start_state), (None, r2.start_state)]

    return NFA(
        num_states=1 + r1.num_states + r2.num_states,
        start_state=0,
        end_states=r1.end_states | r2.end_states,
        transitions=trans)


def UnionsOf(*regs):
    result = epsilon
    for reg in regs:
        result = Union(result, reg)
    return result


def Character(c):
    return NFA(
        num_states=2,
        start_state=0,
        end_states=[1],
        transitions={
            0: [(c, 1)]
        })


def OneOf(chars):
    matcher = lambda x: x in chars
    return Character(matcher)


def Exact(string):
    return ConcatsOf(*[Character(x) for x in string])


def Not(chars):
    matcher = lambda x: x not in chars
    return Character(matcher)


epsilon = NFA(
    num_states=1,
    start_state=0,
    end_states=[0],
    transitions={})
