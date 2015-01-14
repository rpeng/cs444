class NFA(object):
    """Represents a non-deterministic finite automaton"""

    def __init__(self,
                 all_states,   # set of all states
                 start_state,  # start state
                 end_states,   # set of end states
                 transitions   # dictionary of transitions
                 # in form {prev: [(input_or_matcher, next),...],...}
                 ):
        self.all_states = set(all_states)
        self.start_state = start_state
        self.end_states = set(end_states)
        self.transitions = transitions

    def EpsilonClosure(self, states):
        result = set(states)
        worklist = set(states)
        while worklist:
            t = worklist.pop()
            for (matcher, next_state) in self.transitions[t]:
                if matcher is None and next_state not in result:
                    result.add(next_state)
                    worklist.add(next_state)
        return result

    def Executor(self):
        return NFAExecutor(self)

    def ShouldAccept(self, inputs):
        """Runs the automaton on the given inputs

        Returns True if the input is accepted by the atomaton."""
        executor = self.Executor()
        for input_token in inputs:
            executor.Consume(input_token)
        return executor.IsAccepted()


class NFAExecutor(object):
    """The executor will step through the NFA given some input"""
    def __init__(self, nfa):
        self.nfa = nfa
        self.current_states = set([self.nfa.start_state])
        self.current_states = self.nfa.EpsilonClosure(self.current_states)

    def Consume(self, input_token):
        """Consumes a single input and steps through the NFA"""
        new_states = set()
        for state in self.current_states:
            state_trans = self.nfa.transitions[state]
            for (expected_token, next_state) in state_trans:
                if (input_token == expected_token or expected_token is None):
                    new_states.add(next_state)
        self.current_states = self.nfa.EpsilonClosure(new_states)

    def IsAccepted(self):
        """Returns True if the current input sequence is accepted"""
        return not self.current_states.isdisjoint(self.nfa.end_states)
