class EnvStmtMixin(object):
    # Statement
    def VisitBlock(self, node):
        return self.DefaultBehaviour(node)

    def VisitIfThenElseStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitWhileStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitForStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitLocalVarDeclStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitReturnStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitEmptyStatement(self, node):
        return self.DefaultBehaviour(node)
