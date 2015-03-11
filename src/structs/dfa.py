from structs.nfa import NFA


class DFA(object):
    def __init__(self,
                 num_states,
                 start_state,
                 end_states,
                 transitions):
        self.num_states = num_states
        self.start_state = start_state
        self.end_states = set(end_states)
        self.transitions = transitions

    def __eq__(self, other):
        return (self.num_states == other.num_states and
                self.start_state == other.start_state and
                self.end_states == other.end_states and
                self.transitions == other.transitions)

    def ShouldAccept(self, inputs):
        """Runs the automaton on the given inputs

        Returns True if the input is accepted by the atomaton."""
        executor = self.Executor()
        for input_token in inputs:
            executor = executor.Consume(input_token)
        return executor.IsAccepting()

    def Executor(self):
        return DFAExecutor(self)


class DFAExecutor(object):
    error_state = object()

    """The executor will step through the DFA given some input"""
    def __init__(self, dfa, current_state=None):
        self.dfa = dfa
        self.current_state = current_state
        if current_state is None:
            self.current_state = dfa.start_state

    def Consume(self, input_token):
        """Consumes a single input and steps through the NFA"""
        current = self.dfa.transitions.get(self.current_state)
        if current is None:
            return DFAExecutor(self.dfa, self.error_state)

        for matcher, next_state in current.items():
            if (matcher == input_token or
                    callable(matcher) and matcher(input_token)):
                return DFAExecutor(self.dfa, next_state)
        return DFAExecutor(self.dfa, self.error_state)

    def IsAccepting(self):
        """Returns True if the current input sequence is accepted"""
        return self.current_state in self.dfa.end_states

    def IsError(self):
        return self.current_state is self.error_state
