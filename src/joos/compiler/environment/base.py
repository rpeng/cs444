from joos.syntax import ASTVisitor


class EnvBuilder(EnvDeclMixin, EnvExprMixin, EnvStmtMixin, ASTVisitor):
    # Base
    def Visit(self, node):  # Entry point
        return node.visit(self)

    def VisitCompilationUnit(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayType(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassOrInterfaceType(self, node):
        return self.DefaultBehaviour(node)

    def VisitVoidType(self, node):
        return self.DefaultBehaviour(node)

    def VisitPrimitiveType(self, node):
        return self.DefaultBehaviour(node)

    def VisitName(self, node):
        return self.DefaultBehaviour(node)

    def VisitLiteral(self, node):
        return self.DefaultBehaviour(node)
