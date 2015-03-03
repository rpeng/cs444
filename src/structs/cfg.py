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
    def __init__(self, token_type, lexeme='', row=None, col=None):
        self.token_type = token_type
        self.lexeme = lexeme
        self.row = row
        self.col = col

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
        self._ComputeNullables()  # self.nullables
        self._ComputeFirsts()  # self.firsts
        self._ComputeFollows()  # self.follows

    def _ComputeNullables(self):
        self.nullables = dict((symbol, False) for symbol in self.nonterminals)
        while True:
            changed = False
            for r in self.rules:
                if self.nullables[r.lhs]:
                    continue
                if r.rhs is None:
                    changed = True
                    self.nullables[r.lhs] = True
                else:
                    all_nullable = True
                    for symbol in r.rhs:
                        if (symbol in self.terminals
                                or not self.nullables[symbol]):
                            all_nullable = False
                            break
                    if all_nullable:
                        changed = True
                        self.nullables[r.lhs] = True
            if not changed:
                break

    def _ComputeFirsts(self):
        self.firsts = dict((symbol, set()) for symbol in self.nonterminals)
        while True:
            changed = False
            for r in self.rules:
                if r.rhs is None:
                    continue
                lhs_firsts = self.firsts[r.lhs]
                if r.rhs[0] in self.terminals:
                    if r.rhs[0] not in lhs_firsts:
                        self.firsts[r.lhs].add(r.rhs[0])
                        changed = True
                for t in r.rhs:
                    if t not in self.terminals:
                        rhs_firsts = self.firsts[t]
                        new_firsts = lhs_firsts | rhs_firsts
                        if (new_firsts != lhs_firsts):
                            self.firsts[r.lhs] = new_firsts
                            changed = True
                    if not self.Nullable(t):
                        break

            if not changed:
                break

    def _ComputeFollows(self):
        self.follows = dict((symbol, set()) for symbol in self.nonterminals)
        while True:
            changed = False
            for r in self.rules:
                if r.rhs is None:
                    continue
                for i, token in enumerate(r.rhs):
                    if token in self.terminals:
                        continue
                    old = self.follows[token]
                    new = old | self.Firsts(r.rhs[i + 1:])
                    if old != new:
                        self.follows[token] = new
                        changed = True
                    if self.AllNullable(r.rhs[i + 1:]):
                        new = old | self.follows[r.lhs]
                        if old != new:
                            self.follows[token] = new
                            changed = True
            if not changed:
                break

    def Nullable(self, symbol):
        if symbol in self.terminals:
            return False
        return self.nullables[symbol]

    def AllNullable(self, symbols):
        for symbol in symbols:
            if not self.Nullable(symbol):
                return False
        return True

    def First(self, symbol):
        if symbol in self.terminals:
            return set([symbol])
        return self.firsts[symbol]

    def Firsts(self, symbols):
        result = set()
        for symbol in symbols:
            result = result | self.First(symbol)
            if not self.Nullable(symbol):
                break
        return result

    def Follow(self, symbol):
        if symbol in self.terminals:
            return set()
        return self.follows[symbol]

    def __repr__(self):
        rep = "CFG\n"
        rep += "  terminals: {}\n".format(','.join(self.terminals))
        rep += "  nonterminals: {}\n".format(','.join(self.nonterminals))
        rep += "  start: {}\n".format(self.start_symbol)
        rep += "  rules: \n    {}".format('\n    '.join(
            [str(rule) for rule in self.rules]))
        return rep
