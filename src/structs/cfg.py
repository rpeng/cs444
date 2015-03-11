class Rule(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        if self.rhs:
            return "{} -> {}".format(self.lhs, ' '.join(self.rhs))
        else:
            return "{} -> None".format(self.lhs)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)


class Token(object):
    def __init__(self, token_type, lexeme='',
                 row=None, col=None, filename=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.row = row
        self.col = col
        self.filename = filename

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Type: {} Lex: {}".format(self.token_type, self.lexeme)


class CFG(object):
    def __init__(self,
                 terminals,
                 nonterminals,
                 start_symbol,  # must be a nonterminal
                 rules):  # list of (lhs, [rhs...])

        self.terminals = terminals
        self.nonterminals = nonterminals
        self.start_symbol = start_symbol
        self.rules = [Rule(lhs, rhs) for lhs, rhs in rules]

        self.origin_rule = None
        for rule in self.rules:
            if rule.lhs == start_symbol:
                self.origin_rule = rule
                break

        self.all_symbols = self.terminals + self.nonterminals

    def __repr__(self):
        rep = "CFG\n"
        rep += "  terminals: {}\n".format(','.join(self.terminals))
        rep += "  nonterminals: {}\n".format(','.join(self.nonterminals))
        rep += "  start: {}\n".format(self.start_symbol)
        rep += "  rules: \n    {}".format('\n    '.join(
            [str(rule) for rule in self.rules]))
        return rep
