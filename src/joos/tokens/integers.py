from joos.tokens.common import *
from fsa.regexp import *

integer_type_suffix = OneOf('lL')

decimal_numeral = Union(Character('0'),
                        Concat(Character(NonZeroDigitMatcher),
                               ZeroOrMore(java_digit)))

decimal_integer_literal = Concat(decimal_numeral,
                                 Optional(integer_type_suffix))

integer_literal = decimal_integer_literal
