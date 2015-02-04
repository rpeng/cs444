class InvalidToken(Exception):
    def __init__(self, lexeme, row, col):
        self.lexeme = lexeme
        self.row = row
        self.col = col
        self.message = "Unexpected token '{}' on row {}, column {}".format(
            lexeme, row, col)
        super(Exception, self).__init__(self.message)


class EmptyInput(Exception):
    pass
