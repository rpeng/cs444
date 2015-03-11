from joos.tokens.small import *
from structs.converter import NFAToDFA


class TestSmall(object):
    def test_boolean_literal(self):
        re = NFAToDFA(boolean_literal)
        assert re.ShouldAccept('true')
        assert re.ShouldAccept('false')
        assert not re.ShouldAccept('tfa')
        assert not re.ShouldAccept('')

    def test_null_literal(self):
        re = NFAToDFA(null_literal)
        assert re.ShouldAccept('null')
        assert not re.ShouldAccept('')
