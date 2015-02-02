from joos.tokens.small import *

class TestSmall(object):
    def test_boolean_literal(self):
        re = boolean_literal
        assert re.ShouldAccept('true')
        assert re.ShouldAccept('false')
        assert not re.ShouldAccept('tfa')
        assert not re.ShouldAccept('')

    def test_null_literal(self):
        re = null_literal
        assert re.ShouldAccept('null')
        assert not re.ShouldAccept('')
