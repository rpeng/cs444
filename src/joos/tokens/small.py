from structs.regexp import *

boolean_literal = Union(Exact('true'), Exact('false'))
null_literal = Exact('null')
