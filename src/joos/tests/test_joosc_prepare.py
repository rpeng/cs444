from joos.joosc import PrepareTokens
from structs.cfg import Token

from nose.tools import *


class TestJooscPrepare(object):
    def test_strips_whitespace(self):
        tokens = [Token('PUBLIC', 'public', 1, 1),
                  Token('WHITESPACE', ' ', 1, 7),
                  Token('VOID', 'void', 1, 8)]
        result = PrepareTokens(tokens)
        assert_equal(result, [
            Token('BOF', 'BOF'),
            Token('public', 'public', 1, 1),
            Token('void', 'void', 1, 8),
            Token('EOF', 'EOF')
        ])

    def test_converts_types(self):
        tokens = [Token('PUBLIC', 'public', 1, 1),
                  Token('ID', 'Richard', 1, 7),
                  Token('LPAREN', '(', 1, 13),
                  Token('STRING', '"asdf"', 1, 17)]
        result = PrepareTokens(tokens)
        assert_equal(result, [
            Token('BOF', 'BOF'),
            Token('public', 'public', 1, 1),
            Token('ID', 'Richard', 1, 7),
            Token('(', '(', 1, 13),
            Token('STRING', '"asdf"', 1, 17),
            Token('EOF', 'EOF'),
        ])

    def test_raises_on_unsupported(self):
        tokens = [Token('PUBLIC', 'public', 1, 1),
                  Token('WHITESPACE', ' ', 1, 7),
                  Token('DO', 'do', 1, 8)]
        assert_raises(RuntimeError, PrepareTokens, tokens)
