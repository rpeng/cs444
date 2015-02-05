from structs.cfg import Rule, CFG
from compiler.errors import *


class ParseTreeNode(object):
    def __init__(self, token, rule=None, children=None):
        self.token = token
        self.rule = rule
        if children is None:
            self.children = []
        else:
            self.children = children

    def AddChild(self, child):
        self.children.append(child)

    def StrTree(self, indent=0):
        result = " "*indent
        if self.rule:
            result += str(self.rule)
        else:
            result += self.token.lexeme
        result += '\n'
        for child in self.children:
            result += child.StrTree(indent + 2)
        return result

    def __repr__(self):
        if not self.rule:
            return "ParseTreeNode: '{}'".format(self.token.lexeme)
        else:
            return "ParseTreeNode: " + str(self.rule)


def _gen_list(a_string_list):
    for x in a_string_list:
        yield x.strip()


def FromLr1(lr1_input_lines):
    l = _gen_list(lr1_input_lines)

    terminals = []
    nonterminals = []
    rules = []
    parse_table = {}

    n = int(l.next())  # num terminals
    for _ in range(n):
        terminals.append(l.next())

    n = int(l.next())  # num nonterminals
    for _ in range(n):
        nonterminals.append(l.next())
    start_symbol = l.next()

    n = int(l.next())  # num rules
    for _ in range(n):
        tokens = [x for x in l.next().split(' ')]
        lhs = tokens[0]
        if len(tokens) > 1:
            rhs = tokens[1:]
        else:
            rhs = None
        rules.append((lhs, rhs))

    cfg = CFG(terminals, nonterminals, start_symbol, rules)

    _ = l.next()  # num states, ignore
    n = int(l.next())  # num entries

    for _ in range(n):
        start, token, action, context = l.next().split(' ')
        start = int(start)
        context = int(context)
        if start not in parse_table:
            parse_table[start] = {}
        if token not in parse_table[start]:
            parse_table[start][token] = {}
        parse_table[start][token] = (action, context)

    return cfg, parse_table


def Parse(cfg, parse_table, tokens):
    """
    Parses given tokens, using the specified context free grammar, and a parse
    table.

    CFG:
        see structs.cfg.CFG

    Parse table:
    {
        state1: {
            token1: (shift, next_state),
            token2: (reduce, rule),
        },
        state2: {
            ...
        }...
    }
    """
    symbols_stack = []
    states_stack = [0]
    parse_tree = []

    for token in tokens:
        while True:
            state = states_stack[-1]
            if state not in parse_table:
                raise ParseError("Parsed past final state")

            rules = parse_table[state]

            if token.token_type not in rules:
                raise ParseErrorWithToken(token, rules.keys())
            action, context = rules[token.token_type]

            # print state, token, action, context

            if action == 'shift':
                symbols_stack.append(token)
                states_stack.append(context)
                parse_tree.append(ParseTreeNode(token))
                break
            elif action == 'reduce':
                rule = cfg.rules[context]
                if rule.rhs is None:
                    n = 0
                else:
                    n = len(rule.rhs)
                if n > 0:
                    symbols_stack = symbols_stack[:-n]
                    states_stack = states_stack[:-n]

                symbols_stack.append(rule.lhs)
                state = states_stack[-1]
                rules = parse_table[state]
                action, context = rules[rule.lhs]
                states_stack.append(context)

                # Extend parse tree
                children = parse_tree[-n:]
                parse_tree = parse_tree[:-n]
                parse_tree.append(ParseTreeNode(rule.lhs, rule, children))

    # Reduce with origin rule
    rule = cfg.origin_rule
    n = len(rule.rhs)
    if n > 0:
        symbols_stack = symbols_stack[:-n]
        states_stack = states_stack[:-n]
        children = parse_tree[-n:]
        parse_tree = parse_tree[:-n]
        parse_tree.append(ParseTreeNode(rule.lhs, rule, children))
    return parse_tree[0]
