from structs.nfa import NFAExecutor
from structs.cfg import Token
from compiler.errors import *


class _MaximalMunchExecutor(object):
    def __init__(self, nfa_exports, newline_token):
        self.nfa_exports = nfa_exports
        self.newline_token = newline_token

    def StatesWithoutErrors(self, states):
        new_states = []
        for emit, nfa in states:
            if not nfa.IsError():
                new_states.append((emit, nfa))
        return new_states

    def PerformStep(self, states, ch):
        new_states = []
        for emit, nfa in states:
            new_states.append((emit, nfa.Consume(ch)))
        return self.StatesWithoutErrors(new_states)

    def FirstEmit(self, states):
        for emit, nfa in states:
            if nfa.IsAccepting():
                return emit
        return None

    def NewStates(self):
        states = []
        for emit, nfa in self.nfa_exports:
            states.append((emit, NFAExecutor(nfa)))
        return states

    def Consume(self, inputs):
        if not inputs:
            raise EmptyInput("Input file is empty")

        idx = 0
        row = 1
        col = 0
        last_accepting = None
        lexeme = ""
        result = []
        states = self.NewStates()

        while idx < len(inputs):
            col += 1
            ch = inputs[idx]
            states = self.PerformStep(states, ch)
            lexeme += ch

            # Current states have at least one accepting state
            token_type = self.FirstEmit(states)
            if token_type is not None:
                last_accepting = (idx, lexeme, token_type, row, col)
            # No states without errors, rewind machine
            elif not states:
                if last_accepting is None:
                    raise InvalidToken(lexeme, row, col)
                idx, lexeme, token_type, row, col = last_accepting
                states = self.NewStates()
                result.append(Token(
                    token_type, lexeme, row, col - len(lexeme) + 1))
                last_accepting = None
                lexeme = ""
                if token_type is self.newline_token:
                    row += 1
                    col = 0
            idx += 1

        # emit final token
        token_type = self.FirstEmit(states)
        if not token_type:
            raise InvalidToken(lexeme, row, col)
        result.append(Token(token_type, lexeme, row, col - len(lexeme) + 1))
        return result


def Scan(exports, inputs, newline_token=None):
    mm = _MaximalMunchExecutor(exports, newline_token)
    return mm.Consume(inputs)
