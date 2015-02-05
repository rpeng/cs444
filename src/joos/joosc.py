import sys

from structs.cfg import Token
from joos.tokens.exports import all_exports, unsupported, symbols_map
from joos.tokens.token_types import Types as t
from compiler.errors import *
from compiler import scanner, parser


TOKEN_TO_LR1_REPR = dict([(k, v) for k, v in symbols_map])
LR1_REPR_TO_TOKEN = dict([(v, k) for k, v in symbols_map])
SKIP_TOKEN_TYPES = [t.WHITESPACE, t.NEWLINE, t.COMMENT]


def ScanInput(inputs):
    """ Scans an input stream one byte at a time."""
    return scanner.Scan(all_exports,
                        inputs,
                        newline_token=t.NEWLINE)


def PrepareTokens(tokens):
    """ Prepares scanned tokens for parsing.
    1. remove whitespace, line terminators, comments
    2. check for unsupported input types
    3. inserts BOF, EOF
    4. converts token_types to match lr1 strings
    """
    filtered = []
    filtered.append(Token(t.BOF, 'BOF'))
    for token in tokens:
        if token.token_type in SKIP_TOKEN_TYPES:
            continue
        if token.token_type in unsupported:
            raise RuntimeError(("Unsupported token '{}' "
                               "on row {} col {}".format(
                                   token.lexeme, token.row, token.col
                               )))
        # Convert to token representations
        token.token_type = TOKEN_TO_LR1_REPR[token.token_type]
        filtered.append(token)
    filtered.append(Token(t.EOF, 'EOF'))
    for token in filtered:
        print token.token_type, token.row, token.col
    return filtered


def Parse(tokens, lr1_grammar_file):
    """Parses a set of tokens"""
    with open(lr1_grammar_file) as f:
        cfg, parse_table = parser.FromLr1(f)
    try:
        return parser.Parse(cfg, parse_table, tokens)
    except ParseErrorWithToken, e:
        if e.token.token_type == t.EOF:
            raise RuntimeError(("Unexpected token at end of file. "
                                "Expecting one of: {}").format(
                                    ' '.join(e.expected)))
        else:
            raise
