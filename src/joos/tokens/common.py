from fsa.regexp import *


def JavaLetterMatcher(ch):
    return ch.isalpha() or ch == '_' or ch == '$'


def JavaDigitMatcher(ch):
    return ch.isdigit()


def NonZeroDigitMatcher(ch):
    return ch.isdigit() and ch != '0'

CR = '\x0d'
LF = '\x0a'


def ValidCharacterMatcher(ch):
    return 0 <= ord(ch) <= 127


def LineTerminatorMatcher(ch):
    return ch in CR + LF


def InputCharacterMatcher(ch):
    return ValidCharacterMatcher(ch) and not LineTerminatorMatcher(ch)

java_letter = Character(JavaLetterMatcher)
java_digit = Character(JavaDigitMatcher)
java_letter_or_digit = Union(java_letter, java_digit)

digits = OneOrMore(java_digit)
input_character = Character(InputCharacterMatcher)
identifier = Concat(java_letter, ZeroOrMore(java_letter_or_digit))
line_terminator = Union(OneOf(CR + LF), Exact(CR + LF))
whitespace = Union(OneOf('\x20\x09\x0c'), line_terminator)
