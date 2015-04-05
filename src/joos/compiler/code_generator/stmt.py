from joos.compiler.environment import Environment


class StmtCodeMixin(object):
    # Statement
    def VisitBlock(self, node):
        self.DefaultBehaviour(node)

    def VisitIfThenElseStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitWhileStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitForStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitReturnStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitEmptyStatement(self, node):
        self.DefaultBehaviour(node)
