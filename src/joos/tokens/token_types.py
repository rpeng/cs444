def _enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    enums['from_str'] = enums
    return type('Enum', (), enums)

COMMON = ['WHITESPACE', 'NEWLINE', 'ID', 'COMMENT']

KEYWORDS = ['ABSTRACT', 'DEFAULT', 'BOOLEAN', 'DO', 'BREAK', 'DOUBLE', 'BYTE',
            'ELSE', 'CASE', 'EXTENDS', 'CATCH', 'FINAL', 'CHAR', 'FINALLY',
            'CLASS', 'FLOAT', 'CONST', 'FOR', 'CONTINUE', 'GOTO', 'IF',
            'PRIVATE', 'IMPLEMENTS', 'PROTECTED', 'IMPORT', 'PUBLIC',
            'INSTANCEOF', 'RETURN', 'INT', 'SHORT', 'INTERFACE', 'STATIC',
            'LONG', 'STRICTFP', 'NATIVE', 'SUPER', 'NEW', 'SWITCH', 'PACKAGE',
            'SYNCHRONIZED', 'THIS', 'THROW', 'THROWS', 'TRANSIENT', 'TRY',
            'VOID', 'VOLATILE', 'WHILE']

LITERALS = ['INTEGER', 'TRUE', 'FALSE', 'CHARACTER', 'STRING', 'NULL']

SEPARATORS = ['LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LBRACKET', 'RBRACKET',
              'SEMICOLON', 'COMMA', 'DOT']

OPERATORS = ['ASSIGN', 'GT', 'LT', 'BANG', 'TILDE', 'QUESTION_MARK', 'COLON',
             'EQ', 'LE', 'GE', 'NE', 'AND', 'OR', 'INC', 'DEC', 'PLUS',
             'MINUS', 'STAR', 'DIV', 'B_AND', 'B_OR', 'XOR', 'MOD', 'LSHIFT',
             'RSHIFT', 'R_USHIFT', 'PLUS_EQ', 'MINUS_EQ', 'TIMES_EQ', 'DIV_EQ',
             'AND_EQ', 'OR_EQ', 'XOR_EQ', 'MOD_EQ', 'LSHIFT_EQ', 'RSHIFT_EQ',
             'R_USHIFT_EQ']

ALL = COMMON + KEYWORDS + LITERALS + SEPARATORS + OPERATORS

ALL_DICT = dict((token, token) for token in ALL)

Types = _enum(**ALL_DICT)
