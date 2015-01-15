from structures.fsa import regexp


class TestRegexp(object):
    def test_epsilon(self):
        nfa = regexp.epsilon()
        assert not nfa.ShouldAccept('12')
        assert nfa.ShouldAccept('')

    def test_character(self):
        nfa = regexp.character('a')
        assert not nfa.ShouldAccept('12')
        assert not nfa.ShouldAccept('aa')
        assert not nfa.ShouldAccept('')
        assert nfa.ShouldAccept('a')

    def test_concat_simple(self):
        r1 = regexp.character('a')
        r2 = regexp.character('b')
        nfa = regexp.concat(r1, r2)

        assert nfa.ShouldAccept('ab')
        assert not nfa.ShouldAccept('a')
        assert not nfa.ShouldAccept('b')
        assert not nfa.ShouldAccept('')

    def test_concat_edge(self):
        r1 = regexp.character('a')
        r2 = regexp.epsilon()
        nfa = regexp.concat(r1, r2)

        assert not nfa.ShouldAccept('12')
        assert not nfa.ShouldAccept('aa')
        assert not nfa.ShouldAccept('')
        assert nfa.ShouldAccept('a')
