from structures.fsa.regexp import *


def JavaLetterMatcher(ch):
    return ch.isalpha() or ch == '_' or ch == '$'


def JavaDigitMatcher(ch):
    return ch.isdigit()


def NonZeroDigitMatcher(ch):
    return ch.isdigit() and ch != '0'


def IntegerTypeSuffixMatcher(ch):
    return ch in 'lL'

java_letter = Character(JavaLetterMatcher)
java_digit = Character(JavaDigitMatcher)
java_letter_or_digit = Union(java_letter, java_digit)

identifier_or_keyword = Concat(java_letter, ZeroOrMore(java_letter_or_digit))

integer_type_suffix = Character(IntegerTypeSuffixMatcher)

decimal_numeral = Union(Character('0'),
                        Concat(Character(NonZeroDigitMatcher),
                               ZeroOrMore(java_digit)))

decimal_integer_literal = Concat(decimal_numeral,
                                 Optional(integer_type_suffix))
