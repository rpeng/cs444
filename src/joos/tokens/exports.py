from fsa.regexp import *
from joos.tokens.token_types import KEYWORDS, Types as t
from joos.tokens import common, comments, integers, small, strings

# If you update this file, please also update terminals.jcfg
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

unsupported = [
    # unsupported keywords
    t.DEFAULT, t.DO, t.BREAK, t.DOUBLE, t.CASE, t.CATCH, t.FINALLY, t.FLOAT,
    t.CONST, t.CONTINUE, t.GOTO, t.PRIVATE, t.LONG, t.STRICTFP, t.SUPER,
    t.SWITCH, t.SYNCHRONIZED, t.THROW, t.THROWS, t.TRANSIENT, t.TRY, t.VOLATILE,
    # unsupported operators
    t.TILDE, t.QUESTION_MARK, t.COLON, t.INC, t.DEC, t.XOR, t.LSHIFT, t.RSHIFT,
    t.R_USHIFT, t.PLUS_EQ, t.MINUS_EQ, t.TIMES_EQ, t.DIV_EQ, t.AND_EQ, t.OR_EQ,
    t.MOD_EQ, t.LSHIFT_EQ, t.RSHIFT_EQ, t.R_USHIFT_EQ,
]

all_exports = (keyword_exports +
               literal_exports +
               separator_exports +
               operator_exports +
               common_exports)
