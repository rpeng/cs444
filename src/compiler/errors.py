

class InvalidToken(Exception):
    def __init__(self, lexeme, row, col):
        self.lexeme = lexeme
        self.row = row
        self.col = col
        self.message = "Invalid token '{}' on row {}, column {}".format(
            lexeme, row, col)
        super(Exception, self).__init__(self.message)


class EmptyInput(Exception):
    pass


class ParseError(Exception):
    pass


class ParseErrorWithToken(ParseError):
    def __init__(self, token, expected):
        self.token = token
        self.expected = expected
        self.message = "Unexpected token '{}', expecting one of: {}".format(
            self.token, ' '.join(self.expected))
        super(Exception, self).__init__(self.message)
