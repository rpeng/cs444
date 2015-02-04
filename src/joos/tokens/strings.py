from joos.tokens.common import *
from structs.regexp import *


def SingleCharacterMatcher(ch):
    return InputCharacterMatcher(ch) and ch not in "'\\"


def StringCharacterMatcher(ch):
    return InputCharacterMatcher(ch) and ch not in '"\\'

single_quote = Character("'")
double_quote = Character('"')
backslash = Character("\\")

single_character = Character(SingleCharacterMatcher)

zero_to_three = OneOf('0123')
octal_digit = OneOf('01234567')

octal_escape_digits = UnionsOf(
    octal_digit,
    Concat(octal_digit, octal_digit),
    ConcatsOf(zero_to_three, octal_digit, octal_digit))

single_escape_char = OneOf('btnfr"\'\"\\')

escape_sequence = Union(
    Concat(backslash, single_escape_char),
    Concat(backslash, octal_escape_digits))

string_chars = OneOrMore(
    Union(Character(StringCharacterMatcher), escape_sequence))

string_literal = ConcatsOf(
    double_quote, Optional(string_chars), double_quote)

character_literal = Union(
    ConcatsOf(single_quote, single_character, single_quote),
    ConcatsOf(single_quote, escape_sequence, single_quote))
