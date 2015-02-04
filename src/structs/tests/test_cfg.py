from structs.cfg import *

from nose.tools import *


class TestCFG(object):
    def __init__(self):
        self.cfg = CFG(
            terminals="bdpqlz",
            nonterminals="SCD",
            start_symbol="S",
            rules=[
                ('S', ('b', 'S', 'd')),
                ('S', ('p', 'S', 'q')),
                ('S', ('C')),
                ('S', ('D')),
                ('C', ('l', 'C')),
                ('C', None),
                ('D', ('z'))
            ])

    def TestNullables(self):
        assert_true(self.cfg.Nullable('S'))
        assert_true(self.cfg.Nullable('C'))
        assert_true(self.cfg.AllNullable('CS'))
        assert_false(self.cfg.Nullable('D'))

    def TestFirsts(self):
        assert_equal(self.cfg.First('S'), set('bplz'))
        assert_equal(self.cfg.First('C'), set('l'))
        assert_equal(self.cfg.First('D'), set('z'))
        assert_equal(self.cfg.Firsts('DS'), set('z'))
        assert_equal(self.cfg.Firsts('CD'), set('lz'))

    def TestFollows(self):
        assert_equal(self.cfg.Follow('S'), set('qd'))
        assert_equal(self.cfg.Follow('C'), set('qd'))
        assert_equal(self.cfg.Follow('D'), set('qd'))
