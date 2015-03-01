class StmtPrinterMixin(object):
    def VisitBlock(self, node):
        return "TODO"

    def VisitIfThenElseStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitWhileStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitForStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitLocalVarDeclStatement(self, node):
        return self.DefaultBehaviour(node)
