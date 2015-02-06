from joos.tokens.common import *
from structs.regexp import *

integer_type_suffix = OneOf('lL')

decimal_numeral = Union(Character('0'),
                        Concat(Character(NonZeroDigitMatcher),
                               ZeroOrMore(java_digit)))

decimal_integer_literal = decimal_numeral

integer_literal = decimal_numeral
