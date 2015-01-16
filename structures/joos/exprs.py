from structures.fsa.regexp import *


def JavaLetterMatcher(ch):
    return ch.isalpha() or ch == '_' or ch == '$'


def JavaDigitMatcher(ch):
    return ch.isdigit()


def NonZeroDigitMatcher(ch):
    return ch.isdigit() and ch != '0'


java_letter = Character(JavaLetterMatcher)
java_digit = Character(JavaDigitMatcher)
java_letter_or_digit = Union(java_letter, java_digit)

identifier_or_keyword = Concat(java_letter, ZeroOrMore(java_letter_or_digit))

integer_type_suffix = OneOf('lL')

decimal_numeral = Union(Character('0'),
                        Concat(Character(NonZeroDigitMatcher),
                               ZeroOrMore(java_digit)))

decimal_integer_literal = Concat(decimal_numeral,
                                 Optional(integer_type_suffix))

hex_prefix = Concat(Character('0'), OneOf('xX'))
hex_digit = OneOf('0123456789abcdefABCDEF')
hex_integer_literal = Concat(hex_prefix, OneOrMore(hex_digit))

octal_digit = OneOf('01234567')
octal_integer_literal = Concat(Character('0'), OneOrMore(octal_digit))

integer_literal = UnionsOf(decimal_integer_literal,
                           hex_integer_literal,
                           octal_integer_literal)
