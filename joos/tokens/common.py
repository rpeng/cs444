from fsa.regexp import *

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
