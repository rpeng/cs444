from joos.tokens.integers import *


class TestIntegers(object):
    def test_decimal_integer_literal(self):
        re = decimal_integer_literal
        assert re.ShouldAccept('0')
        #assert re.ShouldAccept('0l')
        assert re.ShouldAccept('1')
        assert re.ShouldAccept('12300')
        #assert re.ShouldAccept('12300L')
        assert not re.ShouldAccept('01')
        assert not re.ShouldAccept('1a')
