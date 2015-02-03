from joos.tokens.exports import all_exports
from joos.tokens.token_types import Types
from compiler.scanner import scan


def scan_input(inputs):
    return scan(all_exports,
                inputs,
                newline_token=Types.NEWLINE)
