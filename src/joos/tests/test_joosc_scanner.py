from nose.tools import *

from joos.lex import ScanInput
from structs.cfg import Token
from lexer.errors import *


class TestJooscScanner(object):
    def test_empty(self):
        assert_raises(EmptyInput, ScanInput, "")

    def test_simple(self):
        result = ScanInput("public void main")
        assert_equal(result, [Token('PUBLIC', 'public', 1, 1),
                              Token('WHITESPACE', ' ', 1, 7),
                              Token('VOID', 'void', 1, 8),
                              Token('WHITESPACE', ' ', 1, 12),
                              Token('ID', 'main', 1, 13)])

    def test_int_decl(self):
        result = ScanInput("int i=12")
        assert_equal(result, [Token('INT', 'int', 1, 1),
                              Token('WHITESPACE', ' ', 1, 4),
                              Token('ID', 'i', 1, 5),
                              Token('ASSIGN', '=', 1, 6),
                              Token('INTEGER', '12', 1, 7)])

    def test_string_decl(self):
        result = ScanInput(r"""String s="world\r\t";""")
        assert_equal(result, [Token('ID', 'String', 1, 1),
                              Token('WHITESPACE', ' ', 1, 7),
                              Token('ID', 's', 1, 8),
                              Token('ASSIGN', '=', 1, 9),
                              Token('STRING', r'"world\r\t"', 1, 10),
                              Token('SEMICOLON', ';', 1, 21)])

    def test_error(self):
        assert_raises(InvalidToken, ScanInput, r"""String \ns="world\r\t";""")
