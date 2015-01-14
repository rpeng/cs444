from structures.fsa import nfa


class TestNFA(object):
    def setUp(self):
        # Binary strings where last symbol is 0
        # or contains only 1s
        """
        --------------------------------------------------------------------
        |                               |                                  |
        |                               |                                  |
        |                               |                                  |
        |              +-----+       +--v--+       +-----+       +-----+   |
        |        +-----+  A* <---e---+  B  +---e--->  C  +---0--->  D* |   |
        |        |     +--^--+       +-----+       +-+--^+       +-----+   |
        |        1        |                          |  |                  |
        |        +--------+                       +--+  |                  |
        |                                         |     |                  |
        |                                         +-0,1++                  |
        --------------------------------------------------------------------
        """

        self.nfa = nfa.NFA(
            all_states='abcd',
            start_state='b',
            end_states='ad',
            transitions={
                'a': [('1', 'a')],
                'b': [(None, 'a'), (None, 'c')],
                'c': [('0', 'c'), ('1', 'c'), ('0', 'd')],
                'd': [],
            })

    def test_epsilon_closure(self):
        assert self.nfa.EpsilonClosure('a') == set('a')
        assert self.nfa.EpsilonClosure('bc') == set('abc')
        assert self.nfa.EpsilonClosure('bd') == set('abcd')

    def test_accept(self):
        assert self.nfa.ShouldAccept('')
        assert self.nfa.ShouldAccept('0000')
        assert self.nfa.ShouldAccept('0010')
        assert self.nfa.ShouldAccept('111')
        assert not self.nfa.ShouldAccept('1011')
