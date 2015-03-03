from joos.tokens.common import *


class TestCommon(object):
    def AssertAcceptsRange(self, re, string):
        for x in string:
            assert re.ShouldAccept(x)

    def AssertNotAcceptsRange(self, re, string):
        for x in string:
            assert not re.ShouldAccept(x)

    def test_input_character(self):
        self.AssertAcceptsRange(input_character, '\x04abc\x7F')
        self.AssertNotAcceptsRange(input_character, '\n\r\x80')
        assert not input_character.ShouldAccept('')

    def test_java_letter(self):
        self.AssertAcceptsRange(java_letter, 'abcXYZ$_')
        self.AssertNotAcceptsRange(java_letter, '0@+-()')
        assert not java_letter.ShouldAccept('')

    def test_java_digit(self):
        self.AssertAcceptsRange(java_digit, '0123456789')
        self.AssertNotAcceptsRange(java_digit, '()abcABC$_')

    def test_digits(self):
        re = digits
        assert re.ShouldAccept('01231')
        assert re.ShouldAccept('120')
        assert re.ShouldAccept('000')
        assert not re.ShouldAccept('0a00')
        assert not re.ShouldAccept('')

    def test_java_identifier(self):
        re = identifier
        assert re.ShouldAccept('j')
        assert re.ShouldAccept('jane123')
        assert re.ShouldAccept('$_123')
        assert not re.ShouldAccept('3jane')
        assert not re.ShouldAccept('')
        self.AssertNotAcceptsRange(re, '&*@!#')

    def test_whitespace(self):
        re = whitespace
        assert re.ShouldAccept(' ')
        assert re.ShouldAccept('\x09')
        assert not re.ShouldAccept('j ')
        assert not re.ShouldAccept(' j')
        assert not re.ShouldAccept('kasdjf')

    def test_line_terminator(self):
        re = line_terminator
        assert re.ShouldAccept('\x0a')
        assert re.ShouldAccept('\x0d\x0a')
        assert not re.ShouldAccept(' ')
        assert not re.ShouldAccept('\n\r')
