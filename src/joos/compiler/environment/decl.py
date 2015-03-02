class EnvDeclMixin(object):
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
