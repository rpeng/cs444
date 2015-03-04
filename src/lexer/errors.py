from joos.errors import JoosError


class InvalidToken(JoosError):
    def __init__(self, lexeme=None, row=None, col=None):
        if row is None and col is None:
            super(InvalidToken, self).__init__(lexeme)
        else:
            self.lexeme = lexeme
            self.row = row
            self.col = col
            self.message = "Invalid token '{}' on row {}, column {}".format(
                lexeme, row, col)
            super(InvalidToken, self).__init__(self.message)


class EmptyInput(JoosError):
    pass


class ParseError(JoosError):
    pass


class ParseErrorWithToken(JoosError):
    def __init__(self, token=None, expected=None):
        if isinstance(token, str):
            super(ParseErrorWithToken, self).__init__(token)
        else:
            self.token = token
            self.expected = expected
            self.message = ("Unexpected token '{}' on row {} col {}."
                            " Expecting one of: {}").format(
                self.token.lexeme, self.token.row, self.token.col,
                ' '.join(self.expected))
            super(ParseErrorWithToken, self).__init__(self.message)
