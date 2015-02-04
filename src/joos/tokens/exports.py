from fsa.regexp import *
from joos.tokens.token_types import KEYWORDS, Types as t
from joos.tokens import common, comments, integers, small, strings

# Exported NFAs for maximal munch
keyword_exports = [
    (t.from_str[x], Exact(x.lower())) for x in KEYWORDS
]

literal_exports = [
    (t.INTEGER, integers.integer_literal),
    (t.TRUE, Exact('true')),
    (t.FALSE, Exact('false')),
    (t.CHARACTER, strings.character_literal),
    (t.STRING, strings.string_literal),
    (t.NULL, Exact('null'))
]

separator_exports = [
    (t.LPAREN, Exact('(')),
    (t.RPAREN, Exact(')')),
    (t.LBRACE, Exact('{')),
    (t.RBRACE, Exact('}')),
    (t.LBRACKET, Exact('[')),
    (t.RBRACKET, Exact(']')),
    (t.SEMICOLON, Exact(';')),
    (t.COMMA, Exact(',')),
    (t.DOT, Exact('.'))
]

operator_exports = [
    (t.ASSIGN, Exact('=')),
    (t.GT, Exact('>')),
    (t.BANG, Exact('!')),
    (t.TILDE, Exact('~')),
    (t.QUESTION_MARK, Exact('?')),
    (t.COLON, Exact(':')),
    (t.EQ, Exact('==')),
    (t.LE, Exact('<=')),
    (t.GE, Exact('>=')),
    (t.NE, Exact('!=')),
    (t.AND, Exact('&&')),
    (t.OR, Exact('||')),
    (t.INC, Exact('++')),
    (t.DEC, Exact('--')),
    (t.PLUS, Exact('+')),
    (t.MINUS, Exact('-')),
    (t.STAR, Exact('*')),
    (t.DIV, Exact('/')),
    (t.B_AND, Exact('&')),
    (t.B_OR, Exact('|')),
    (t.XOR, Exact('^')),
    (t.MOD, Exact('%')),
    (t.LSHIFT, Exact('<<')),
    (t.RSHIFT, Exact('>>')),
    (t.R_USHIFT, Exact('>>>')),
    (t.PLUS_EQ, Exact('+=')),
    (t.MINUS_EQ, Exact('-=')),
    (t.TIMES_EQ, Exact('*=')),
    (t.DIV_EQ, Exact('/=')),
    (t.AND_EQ, Exact('&=')),
    (t.OR_EQ, Exact('|=')),
    (t.XOR_EQ, Exact('^=')),
    (t.MOD_EQ, Exact('%=')),
    (t.LSHIFT_EQ, Exact('<<=')),
    (t.RSHIFT_EQ, Exact('>>=')),
    (t.R_USHIFT_EQ, Exact('>>>='))
]

common_exports = [
    (t.WHITESPACE, common.whitespace),
    (t.NEWLINE, common.line_terminator),
    (t.ID, common.identifier),
    (t.COMMENT, comments.comment)
]

all_exports = (keyword_exports +
               literal_exports +
               separator_exports +
               operator_exports +
               common_exports)
