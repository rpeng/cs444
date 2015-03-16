class StmtPrinterMixin(object):
    def VisitBlock(self, node):
        return """{i}Block:
{i}  Statements:
{statements}""".format(i=self.i(), statements=self.ns(node.stmts))

    def VisitIfThenElseStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitWhileStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitForStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitLocalVarDeclStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitReturnStatement(self, node):
        return """{i}ReturnStatement:
{i}  Expression:
{e}""".format(i=self.i(),e=self.n(node.exp))
