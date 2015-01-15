from structures.fsa import regexp


class TestRegexp(object):
    def test_epsilon(self):
        nfa = regexp.epsilon
        assert not nfa.ShouldAccept('12')
        assert nfa.ShouldAccept('')

    def test_character(self):
        nfa = regexp.Character('a')
        assert not nfa.ShouldAccept('12')
        assert not nfa.ShouldAccept('aa')
        assert not nfa.ShouldAccept('')
        assert nfa.ShouldAccept('a')

    def test_character_matcher(self):
        nfa = regexp.Character(lambda x: x.isalpha())
        assert nfa.ShouldAccept('a')
        assert nfa.ShouldAccept('b')
        assert not nfa.ShouldAccept('2')

    def test_concat_simple(self):
        r1 = regexp.Character('a')
        r2 = regexp.Character('b')
        nfa = regexp.Concat(r1, r2)

        assert nfa.ShouldAccept('ab')
        assert not nfa.ShouldAccept('a')
        assert not nfa.ShouldAccept('b')
        assert not nfa.ShouldAccept('')

    def test_concat_edge(self):
        r1 = regexp.Character('a')
        r2 = regexp.epsilon
        nfa = regexp.Concat(r1, r2)

        assert not nfa.ShouldAccept('12')
        assert not nfa.ShouldAccept('aa')
        assert not nfa.ShouldAccept('')
        assert nfa.ShouldAccept('a')

    def test_zero_or_more(self):
        r = regexp.ZeroOrMore(regexp.Character('a'))
        assert r.ShouldAccept('')
        assert r.ShouldAccept('a')
        assert r.ShouldAccept('aaa')
        assert not r.ShouldAccept('aab')

    def test_union_simple(self):
        r1 = regexp.Character('a')
        r2 = regexp.Character('b')
        union = regexp.Union(r1, r2)

        assert union.ShouldAccept('a')
        assert union.ShouldAccept('b')
        assert not union.ShouldAccept('')
        assert not union.ShouldAccept('aa')
