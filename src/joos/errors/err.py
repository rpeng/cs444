class JoosError(RuntimeError):
    pass


def err(token, msg):
    string = "Row {} col {}: {}".format(token.row, token.col, msg)
    raise JoosError(string)
