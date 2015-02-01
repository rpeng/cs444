from fsa import regexp


class TestRegexp(object):
    def test_epsilon(self):
        re = regexp.epsilon
        assert not re.ShouldAccept('12')
        assert re.ShouldAccept('')

    def test_character(self):
        re = regexp.Character('a')
        assert not re.ShouldAccept('12')
        assert not re.ShouldAccept('aa')
        assert not re.ShouldAccept('')
        assert re.ShouldAccept('a')

    def test_character_matcher(self):
        re = regexp.Character(lambda x: x.isalpha())
        assert re.ShouldAccept('a')
        assert re.ShouldAccept('b')
        assert not re.ShouldAccept('2')

    def test_one_of(self):
        re = regexp.OneOf('abc')
        assert re.ShouldAccept('a')
        assert re.ShouldAccept('b')
        assert re.ShouldAccept('c')
        assert not re.ShouldAccept('2')

    def test_concat_simple(self):
        r1 = regexp.Character('a')
        r2 = regexp.Character('b')
        re = regexp.Concat(r1, r2)

        assert re.ShouldAccept('ab')
        assert not re.ShouldAccept('a')
        assert not re.ShouldAccept('b')
        assert not re.ShouldAccept('')

    def test_concat_edge(self):
        r1 = regexp.Character('a')
        r2 = regexp.epsilon
        re = regexp.Concat(r1, r2)

        assert not re.ShouldAccept('12')
        assert not re.ShouldAccept('aa')
        assert not re.ShouldAccept('')
        assert re.ShouldAccept('a')

    def test_optional(self):
        r = regexp.Character('a')
        opt = regexp.Optional(r)

        assert opt.ShouldAccept('a')
        assert opt.ShouldAccept('')
        assert not opt.ShouldAccept('b')

    def test_one_or_more(self):
        r = regexp.Character('a')
        opt = regexp.OneOrMore(r)

        assert opt.ShouldAccept('a')
        assert opt.ShouldAccept('aaa')
        assert not opt.ShouldAccept('b')

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

    def test_unions_of(self):
        r1 = regexp.Character('a')
        r2 = regexp.Character('b')
        r3 = regexp.Character('c')
        union = regexp.UnionsOf(r1, r2, r3)

        assert union.ShouldAccept('a')
        assert union.ShouldAccept('b')
        assert union.ShouldAccept('c')
        assert not union.ShouldAccept('d')
