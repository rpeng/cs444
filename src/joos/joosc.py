from joos.tokens.exports import all_exports
from joos.tokens.token_types import Types
from compiler.scanner import Scan


def ScanInput(inputs):
    return Scan(all_exports,
                inputs,
                newline_token=Types.NEWLINE)


def ScanFile(input_file):
    source = None
    with open(input_file) as f:
        source = f.read()
    return ScanInput(source)
