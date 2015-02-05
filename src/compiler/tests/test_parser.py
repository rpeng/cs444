from structs.cfg import CFG
from compiler.parser import parse, from_lr1
from compiler.errors import *

from nose.tools import *

SAMPLE_LR1_PATH = 'compiler/tests/fixtures/sample.lr1'


class TestParser(object):
    cfg = None
    parse_table = None

    @classmethod
    def setupClass(cls):
        with open(SAMPLE_LR1_PATH) as f:
            cls.cfg, cls.parse_table = from_lr1(f.readlines())

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
        tree = parse(self.cfg, self.parse_table, [
            'BOF', '(', 'id', '-', 'id', ')', 'EOF'
        ])
        assert_equal(expected_tree, tree.StrTree())

    def test_parser_error_past_eof(self):
        tokens = ['BOF', '(', 'id', '-', 'id', ')', 'EOF', 'e']
        assert_raises(ParseError, parse, self.cfg, self.parse_table, tokens)

    def test_parser_error_invalid_token(self):
        tokens = ['BOF', '(', 'id', '-', 'id', '(', 'EOF']
        assert_raises(ParseErrorWithToken, parse, self.cfg, self.parse_table,
                      tokens)
