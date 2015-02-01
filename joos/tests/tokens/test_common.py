from joos.tokens.common import *


class TestExprs(object):

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

    def test_java_identifier_or_keyword(self):
        re = identifier_or_keyword
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
        assert re.ShouldAccept('\x0a')
        assert re.ShouldAccept('\x0d\x0a')
        assert not re.ShouldAccept('j ')
        assert not re.ShouldAccept(' j')
        assert not re.ShouldAccept('kasdjf')
