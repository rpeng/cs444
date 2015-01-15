from structures.fsa import nfa


class TestNFA(object):
    def setUp(self):
        # Binary strings where last symbol is 0
        # or contains only 1s
        """
        -----------------------------------------------------------
        |                        |                                |
        |                        |                                |
        |       +-----+       +--v--+       +-----+       +-----+ |
        | +-----+  0* <---e---+  1  +---e--->  2  +---0--->  3* | |
        | |     +--^--+       +-----+       +-+--^+       +-----+ |
        | 1        |                          |  |                |
        | +--------+                       +--+  |                |
        |                                  |     |                |
        |                                  +-0,1++                |
        -----------------------------------------------------------
        """

        self.nfa = nfa.NFA(
            num_states=4,
            start_state=1,
            end_states=[0, 3],
            transitions={
                0: [('1', 0)],
                1: [(None, 0), (None, 2)],
                2: [('0', 2), ('1', 2), ('0', 3)],
            })

    def test_epsilon_closure(self):
        assert self.nfa.EpsilonClosure([0]) == set([0])
        assert self.nfa.EpsilonClosure([1, 2]) == set([0, 1, 2])
        assert self.nfa.EpsilonClosure([1, 3]) == set([0, 1, 2, 3])

    def test_offset(self):
        offset = self.nfa.Offset(3)
        assert offset == nfa.NFA(
            num_states=4,
            start_state=4,
            end_states=[3, 6],
            transitions={
                3: [('1', 3)],
                4: [(None, 3), (None, 5)],
                5: [('0', 5), ('1', 5), ('0', 6)],
            })

    def test_accept(self):
        assert self.nfa.ShouldAccept('')
        assert self.nfa.ShouldAccept('0000')
        assert self.nfa.ShouldAccept('0010')
        assert self.nfa.ShouldAccept('111')
        assert not self.nfa.ShouldAccept('1011')
