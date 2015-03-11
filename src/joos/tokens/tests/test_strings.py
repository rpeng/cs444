from joos.tokens.strings import *
from structs.converter import NFAToDFA


class TestStrings(object):
    def test_character_literal(self):
        re = NFAToDFA(character_literal)
        assert re.ShouldAccept(r"'a'")
        assert re.ShouldAccept(r"'z'")
        assert re.ShouldAccept(r"'0'")
        assert re.ShouldAccept(r"'\012'")
        assert re.ShouldAccept(r"'\t'")
        assert re.ShouldAccept(r"'\''")
        assert re.ShouldAccept(r"'\\'")
        assert not re.ShouldAccept(r"''")
        assert not re.ShouldAccept(r"'12'")
        assert not re.ShouldAccept(r"'2\n'")

    def test_string_literal(self):
        re = NFAToDFA(string_literal)
        assert re.ShouldAccept(r'"a"')
        assert re.ShouldAccept(r'"jano\ni\"s\ta\012bot"')
        assert re.ShouldAccept(r'""')
        assert not re.ShouldAccept(r'""asdf"')
        assert not re.ShouldAccept(r'"\"asdf""')
