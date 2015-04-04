from joos.compiler.environment import Environment


class DeclCodeMixin(object):
    def VisitPackageDecl(self, node):
        raise NotImplementedError

    def VisitImportDecl(self, node):
        raise NotImplementedError

    def VisitClassDecl(self, node):
        raise NotImplementedError

    def VisitInterfaceDecl(self, node):
        raise NotImplementedError

    def VisitMethodDecl(self, node):
        raise NotImplementedError

    def VisitMethodHeader(self, node):
        raise NotImplementedError

    def VisitFieldDecl(self, node):
        raise NotImplementedError

    def VisitConstructorDecl(self, node):
        raise NotImplementedError

    def VisitVariableDeclarator(self, node):
        raise NotImplementedError

    def VisitLocalVarDecl(self, node):
        raise NotImplementedError

    def VisitParameter(self, node):
        raise NotImplementedError
