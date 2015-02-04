from fsa.regexp import *
from compiler.errors import *
from compiler.scanner import scan, Token

from nose.tools import *


def CatchException(method, *args, **kwargs):
    try:
        method(*args, **kwargs)
    except Exception, e:
        return e
    return None


class TestScanner(object):
    def test_empty(self):
        assert_raises(EmptyInput, scan, [], "")

    def test_mm_simple(self):
        exports = [('ONE', Exact('AAA')), ('TWO', Exact('AA'))]
        result = scan(exports, 'AAAAA')
        assert_equal(result, [Token('ONE', 'AAA', 1, 1),
                              Token('TWO', 'AA', 1, 4)])

    def test_mm_more_advanced(self):
        exports = [('KW', UnionsOf(Exact('HELLO'), Exact('WORLD'))),
                   ('ID', OneOrMore(OneOf('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))),
                   ('WS', Exact(' '))]
        result = scan(exports, 'HELLO ABCD WORLD')
        assert_equal(result, [Token('KW', 'HELLO', 1, 1),
                              Token('WS', ' ', 1, 6),
                              Token('ID', 'ABCD', 1, 7),
                              Token('WS', ' ', 1, 11),
                              Token('KW', 'WORLD', 1, 12)])

    def test_mm_more_advanced_error(self):
        exports = [('KW', UnionsOf(Exact('HELLO'), Exact('WORLD'))),
                   ('ID', OneOrMore(OneOf('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))),
                   ('WS', Exact(' '))]
        e = CatchException(scan, exports, "HELLO A123 WORLD")
        assert_equal(e.lexeme, '1')
        assert_equal(e.row, 1)
        assert_equal(e.col, 8)
        print e

    def test_mm_with_crlf(self):
        exports = [('ID', OneOrMore(OneOf('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))),
                   ('SPACES', OneOrMore(OneOf(' '))),
                   ('NEWLINE', Union(OneOf('\r\n'), Exact('\r\n')))]
        result = scan(exports, "A\r\nB \nC\r\rD", newline_token='NEWLINE')
        assert_equal(result, [Token('ID', 'A', 1, 1),
                              Token('NEWLINE', '\r\n', 1, 2),
                              Token('ID', 'B', 2, 1),
                              Token('SPACES', ' ', 2, 2),
                              Token('NEWLINE', '\n', 2, 3),
                              Token('ID', 'C', 3, 1),
                              Token('NEWLINE', '\r', 3, 2),
                              Token('NEWLINE', '\r', 4, 1),
                              Token('ID', 'D', 5, 1)])
