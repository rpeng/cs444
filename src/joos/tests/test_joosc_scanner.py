from joos.joosc import scan_input
from compiler.scanner import Token
from compiler.errors import *

from nose.tools import *


class TestJooscScanner(object):
    def test_empty(self):
        assert_raises(EmptyInput, scan_input, "")

    def test_simple(self):
        result = scan_input("public void main")
        assert_equal(result, [Token('PUBLIC', 'public', 1, 1),
                              Token('WHITESPACE', ' ', 1, 7),
                              Token('VOID', 'void', 1, 8),
                              Token('WHITESPACE', ' ', 1, 12),
                              Token('ID', 'main', 1, 13)])

    def test_int_decl(self):
        result = scan_input("int i=12")
        assert_equal(result, [Token('INT', 'int', 1, 1),
                              Token('WHITESPACE', ' ', 1, 4),
                              Token('ID', 'i', 1, 5),
                              Token('ASSIGN', '=', 1, 6),
                              Token('INTEGER', '12', 1, 7)])

    def test_string_decl(self):
        result = scan_input(r"""String s="world\r\t";""")
        assert_equal(result, [Token('ID', 'String', 1, 1),
                              Token('WHITESPACE', ' ', 1, 7),
                              Token('ID', 's', 1, 8),
                              Token('ASSIGN', '=', 1, 9),
                              Token('STRING', r'"world\r\t"', 1, 10),
                              Token('SEMICOLON', ';', 1, 21)])

    def test_error(self):
        assert_raises(InvalidToken, scan_input, r"""String \ns="world\r\t";""")
