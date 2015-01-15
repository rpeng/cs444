class NFA(object):
    """Represents a non-deterministic finite automaton"""

    def __init__(self,
                 num_states,   # number of states
                 start_state,  # start state
                 end_states,   # set of end states
                 transitions   # dictionary of transitions
                 # in form {prev: [(matcher, next),...],...}
                 # where matcher can be:
                 #     a character: exact character match
                 #     a function: match if matcher(c) == True
                 #     None: Epsilon match
                 ):
        self.num_states = num_states
        self.start_state = start_state
        self.end_states = set(end_states)
        self.transitions = transitions

    def __eq__(self, other):
        return (self.num_states == other.num_states and
                self.start_state == other.start_state and
                self.end_states == other.end_states and
                self.transitions == other.transitions)

    def Offset(self, offset):
        """
        Creates a new NFA, with all states offset by a number.
        Useful for combining NFAs.
        """
        offset_trans = {}
        for key, value in self.transitions.items():
            offset_trans[key+offset] = [(x, y+offset) for x, y in value]

        return NFA(
            num_states=self.num_states,
            start_state=self.start_state + offset,
            end_states=[x+offset for x in self.end_states],
            transitions=offset_trans)

    def EpsilonClosure(self, states):
        """
        Set of all states that can be reached in zero or more
        epsilon moves from each state in states
        """
        result = set(states)
        worklist = set(states)
        while worklist:
            t = worklist.pop()
            if t in self.transitions:
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
            if state in self.nfa.transitions:
                state_trans = self.nfa.transitions[state]
                for (matcher, next_state) in state_trans:
                    if (matcher == input_token or
                            callable(matcher) and matcher(input_token)):
                        new_states.add(next_state)
        self.current_states = self.nfa.EpsilonClosure(new_states)

    def IsAccepted(self):
        """Returns True if the current input sequence is accepted"""
        return not self.current_states.isdisjoint(self.nfa.end_states)
