class ASTVisitor(object):
    """ Abstract visitor class that visits a parse tree node """

    def DefaultBehaviour(self, node):
        raise NotImplementedError

    def VisitParseTreeNode(self, node):
        return self.DefaultBehaviour(node)

    # Base
    def VisitCompilationUnit(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayType(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassOrInterfaceType(self, node):
        return self.DefaultBehaviour(node)

    def VisitPrimitiveType(self, node):
        return self.DefaultBehaviour(node)

    def VisitName(self, node):
        return self.DefaultBehaviour(node)

    def VisitLiteral(self, node):
        return self.DefaultBehaviour(node)

    # Decl
    def VisitPackageDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitImportDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitInterfaceDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodHeader(self, node):
        return self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitConstructorDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitVariableDeclarator(self, node):
        return self.DefaultBehaviour(node)

    def VisitLocalVarDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        return self.DefaultBehaviour(node)

    # Expression
    def VisitAssignmentExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitBinaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitUnaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitCastExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitFieldAccess(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayAccess(self, node):
        return self.DefaultBehaviour(node)

    def VisitThisExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitStatementExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassInstanceCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        return self.DefaultBehaviour(node)

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
