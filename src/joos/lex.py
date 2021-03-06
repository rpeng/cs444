from structs.cfg import Token
from joos.tokens.exports import all_exports, unsupported, symbols_map
from joos.tokens.token_types import Types as t
from lexer.errors import *
from lexer import scanner, parser


TOKEN_TO_LR1_REPR = dict([(k, v) for k, v in symbols_map])
LR1_REPR_TO_TOKEN = dict([(v, k) for k, v in symbols_map])
SKIP_TOKEN_TYPES = [t.WHITESPACE, t.NEWLINE, t.COMMENT]


cfg = None
parse_table = None


def ScanInput(inputs):
    """ Scans an input stream one byte at a time."""
    return scanner.Scan(all_exports,
                        inputs,
                        newline_token=t.NEWLINE)


def PrepareTokens(tokens, filename):
    """ Prepares scanned tokens for parsing.
    1. remove whitespace, line terminators, comments
    2. check for unsupported input types
    3. inserts BOF, EOF, and filename
    4. converts token_types to match lr1 strings
    """
    filtered = []
    filtered.append(Token(t.BOF, 'BOF'))
    for token in tokens:
        if token.token_type in SKIP_TOKEN_TYPES:
            continue
        if token.token_type in unsupported:
            raise JoosError(
                "File: {} \nUnsupported token '{}' on row {} col {}"
                .format(token.filename, token.lexeme, token.row, token.col))
        # Convert to token representations
        token.token_type = TOKEN_TO_LR1_REPR[token.token_type]
        token.filename = filename
        filtered.append(token)
    filtered.append(Token(t.EOF, 'EOF'))
    return filtered


def Parse(tokens, lr1_grammar_file):
    global cfg, parse_table
    """Parses a set of tokens"""
    if not cfg or not parse_table:
        with open(lr1_grammar_file) as f:
            cfg, parse_table = parser.FromLr1(f)
    try:
        return parser.Parse(cfg, parse_table, tokens)[1]
    except ParseErrorWithToken, e:
        if e.token.token_type == t.EOF:
            raise JoosError("File: {} \nUnexpected token at end of file. "
                            "Expecting one of: {}".format(
                                e.token.filename,
                                ' '.join(e.expected)))
        else:
            raise
