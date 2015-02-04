from joos.tokens.exports import all_exports
from joos.tokens.token_types import Types
from compiler.scanner import scan


def scan_input(inputs):
    return scan(all_exports,
                inputs,
                newline_token=Types.NEWLINE)


def scan_file(input_file):
    source = None
    with open(input_file) as f:
        source = f.read()
    return scan_input(source)
