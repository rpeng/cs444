from joos.tokens.common import *

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
