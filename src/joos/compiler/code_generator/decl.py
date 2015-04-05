class DeclCodeMixin(object):
    def VisitPackageDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitImportDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitClassDecl(self, node):
        self.writer.OutputLine("; Code for class decl")
        # .data
        self.writer.OutputLine("; VTable for class decl")
        self.writer.OutputLine("; Name for class decl")
        # .bss
        self.writer.OutputLine("; Statics for class decl")
        self.writer.OutputLine("; Methods for class decl")

        import ipdb; ipdb.set_trace();
        self.DefaultBehaviour(node)

    def VisitInterfaceDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodHeader(self, node):
        self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitConstructorDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitVariableDeclarator(self, node):
        self.DefaultBehaviour(node)

    def VisitLocalVarDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        self.DefaultBehaviour(node)
