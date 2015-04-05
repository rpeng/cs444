from joos.compiler.environment import Environment


class StmtCodeMixin(object):
    # Statement
    def VisitBlock(self, node):
        self.vars = self.vars.NewBlock()
        self.Visit(node.stmts)
        self.vars = self.vars.EndBlock()

    def VisitIfThenElseStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitWhileStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitForStatement(self, node):
        self.DefaultBehaviour(node)

    def VisitReturnStatement(self, node):
        if node.exp:
            self.Visit(node.exp)
        self.writer.OutputLine('leave')
        self.writer.OutputLine('ret')

    def VisitEmptyStatement(self, node):
        pass
