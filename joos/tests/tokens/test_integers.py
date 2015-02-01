from joos.tokens.integers import *


class TestExprs(object):
    def test_decimal_integer_literal(self):
        re = decimal_integer_literal
        assert re.ShouldAccept('0')
        assert re.ShouldAccept('0l')
        assert re.ShouldAccept('1')
        assert re.ShouldAccept('12300')
        assert re.ShouldAccept('12300L')
        assert not re.ShouldAccept('01')
        assert not re.ShouldAccept('1a')

    def test_hex_integer_literal(self):
        re = hex_integer_literal
        assert re.ShouldAccept('0x0')
        assert re.ShouldAccept('0X12FD')
        assert re.ShouldAccept('0xDEABEEF')
        assert not re.ShouldAccept('0xAG')
        assert not re.ShouldAccept('xAG')
        assert not re.ShouldAccept('0x')

    def test_octal_integer_literal(self):
        re = octal_integer_literal
        assert re.ShouldAccept('00')
        assert re.ShouldAccept('0176')
        assert not re.ShouldAccept('0')
        assert not re.ShouldAccept('08')
        assert not re.ShouldAccept('abc')

    def test_integer_literal(self):
        re = integer_literal
        assert re.ShouldAccept('1234')
        assert re.ShouldAccept('0176')
        assert re.ShouldAccept('0xDEAF123')
        assert not re.ShouldAccept('xAG')
        assert not re.ShouldAccept('018')
        assert not re.ShouldAccept('abc')
