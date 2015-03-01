from structs.cfg import CFG, Token
from lexer.parser import Parse, FromLr1
from lexer.errors import *

from nose.tools import *

SAMPLE_LR1_PATH = 'lexer/tests/fixtures/sample.lr1'


def _tokenate(a_list):
    return [Token(x, x) for x in a_list]


class TestParser(object):
    cfg = None
    parse_table = None

    @classmethod
    def setupClass(cls):
        with open(SAMPLE_LR1_PATH) as f:
            cls.cfg, cls.parse_table = FromLr1(f.readlines())

    def test_parser_subtract_parens(self):
        expected_tree = """S -> BOF expr EOF
  BOF
  expr -> term
    term -> ( expr )
      (
      expr -> expr - term
        expr -> term
          term -> id
            id
        -
        term -> id
          id
      )
  EOF
"""
        tree = Parse(self.cfg, self.parse_table, _tokenate([
            'BOF', '(', 'id', '-', 'id', ')', 'EOF'
        ]))
        assert_equal(expected_tree, tree.StrTree())

    def test_parser_error_past_eof(self):
        tokens = _tokenate(['BOF', '(', 'id', '-', 'id', ')', 'EOF', 'e'])
        assert_raises(ParseError, Parse, self.cfg, self.parse_table, tokens)

    def test_parser_error_invalid_token(self):
        tokens = _tokenate(['BOF', '(', 'id', '-', 'id', '(', 'EOF'])
        assert_raises(ParseErrorWithToken, Parse, self.cfg, self.parse_table,
                      tokens)
