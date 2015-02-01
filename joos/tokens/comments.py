from joos.tokens.common import *


def NotSlashOrStarMatcher(ch):
    return ch not in '/*'


def NotStarMatcher(ch):
    return ch not in '*'


traditional_comment = NFA(
    num_states=5,
    start_state=0,
    end_states=[4],
    transitions={
        0: [('/', 1)],
        1: [('*', 2)],
        2: [(NotStarMatcher, 2), ('*', 3)],
        3: [('*', 3), (NotSlashOrStarMatcher, 2), ('/', 4)],
    }
)

end_of_line_comment = ConcatsOf(Exact('//'),
                                ZeroOrMore(input_character),
                                line_terminator)

comment = Union(traditional_comment, end_of_line_comment)
