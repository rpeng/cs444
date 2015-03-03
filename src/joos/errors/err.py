class JoosError(RuntimeError):
    pass


def err(token, msg):
    string = "File: {}\nRow {} col {}: {}".format(
        token.filename, token.row, token.col, msg)
    raise JoosError(string)
