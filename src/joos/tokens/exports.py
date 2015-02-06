from structs.regexp import *
from joos.tokens.token_types import KEYWORDS, Types as t
from joos.tokens import common, comments, integers, small, strings

# If you update this file, please also update terminals.jcfg
# Exported NFAs for maximal munch

# MAPS (token -> string repr)

keyword_map = [
    (t.from_str[x], x.lower()) for x in KEYWORDS
]

literal_map = [
    (t.TRUE, 'true'),
    (t.FALSE, 'false'),
    (t.NULL, 'null'),
    (t.INTEGER, 'INT'),
    (t.CHARACTER, 'CHAR'),
    (t.STRING, 'STRING'),
    (t.MAXINT, '2147483648')
]

separator_map = [
    (t.LPAREN, '('),
    (t.RPAREN, ')'),
    (t.LBRACE, '{'),
    (t.RBRACE, '}'),
    (t.LBRACKET, '['),
    (t.RBRACKET, ']'),
    (t.SEMICOLON, ';'),
    (t.COMMA, ','),
    (t.DOT, '.')
]

operator_map = [
    (t.ASSIGN, '='),
    (t.GT, '>'),
    (t.LT, '<'),
    (t.BANG, '!'),
    (t.TILDE, '~'),
    (t.QUESTION_MARK, '?'),
    (t.COLON, ':'),
    (t.EQ, '=='),
    (t.LE, '<='),
    (t.GE, '>='),
    (t.NE, '!='),
    (t.AND, '&&'),
    (t.OR, '||'),
    (t.INC, '++'),
    (t.DEC, '--'),
    (t.PLUS, '+'),
    (t.MINUS, '-'),
    (t.STAR, '*'),
    (t.DIV, '/'),
    (t.B_AND, '&'),
    (t.B_OR, '|'),
    (t.XOR, '^'),
    (t.MOD, '%'),
    (t.LSHIFT, '<<'),
    (t.RSHIFT, '>>'),
    (t.R_USHIFT, '>>>'),
    (t.PLUS_EQ, '+='),
    (t.MINUS_EQ, '-='),
    (t.TIMES_EQ, '*='),
    (t.DIV_EQ, '/='),
    (t.AND_EQ, '&='),
    (t.OR_EQ, '|='),
    (t.XOR_EQ, '^='),
    (t.MOD_EQ, '%='),
    (t.LSHIFT_EQ, '<<='),
    (t.RSHIFT_EQ, '>>='),
    (t.R_USHIFT_EQ, '>>>=')
]

common_map = [
    (t.WHITESPACE, 'WHITESPACE'),
    (t.NEWLINE, 'LINEBREAK'),
    (t.ID, 'ID'),
    (t.COMMENT, 'COMMENT'),
    (t.BOF, 'BOF'),
    (t.EOF, 'EOF')
]

# EXPORTS: toke -> dfa
keyword_exports = [
    (k, Exact(v)) for k, v in keyword_map
]

literal_exports = [
    (t.TRUE, Exact('true')),
    (t.FALSE, Exact('false')),
    (t.NULL, Exact('null')),
    (t.MAXINT, Exact('2147483648')),
    (t.INTEGER, integers.integer_literal),
    (t.CHARACTER, strings.character_literal),
    (t.STRING, strings.string_literal),
]

separator_exports = [(k, Exact(v)) for k, v in separator_map]

operator_exports = [(k, Exact(v)) for k, v in operator_map]

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
    t.SWITCH, t.SYNCHRONIZED, t.THROW, t.THROWS, t.TRANSIENT, t.TRY,
    t.VOLATILE,
    # unsupported operators
    t.TILDE, t.QUESTION_MARK, t.COLON, t.INC, t.DEC, t.XOR, t.LSHIFT, t.RSHIFT,
    t.R_USHIFT, t.PLUS_EQ, t.MINUS_EQ, t.TIMES_EQ, t.DIV_EQ, t.AND_EQ, t.OR_EQ,
    t.MOD_EQ, t.LSHIFT_EQ, t.RSHIFT_EQ, t.R_USHIFT_EQ,
]


# module exports
symbols_map = (keyword_map +
               literal_map +
               separator_map +
               operator_map +
               common_map)


all_exports = (keyword_exports +
               literal_exports +
               separator_exports +
               operator_exports +
               common_exports)
