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
        self.Visit(node.constructor_decls)
        self.Visit(node.method_decls)

    def VisitInterfaceDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        # link the methods globally
        method_name = self.namer.Visit(node)
        self.writer.DefineGlobalLabel(method_name)
        self.writer.OutputLine('push ebp, esp')
        self.writer.OutputLine('mov ebp, esp')

        self.writer.OutputLine('; method body')
        #TODO self.Visit(node.body_block)

        self.writer.OutputLine('leave')
        self.writer.OutputLine('ret')
        self.writer.OutputLine('')

    def VisitMethodHeader(self, node):
        self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitConstructorDecl(self, node):
        # link the methods globally
        constructor_name = self.namer.Visit(node)
        self.writer.DefineGlobalLabel(constructor_name)
        self.writer.OutputLine('push ebp, esp')
        self.writer.OutputLine('mov ebp, esp')

        self.writer.OutputLine('; constructor body')
        #TODO self.Visit(node.body)

        self.writer.OutputLine('leave')
        self.writer.OutputLine('ret')
        self.writer.OutputLine('')

    def VisitVariableDeclarator(self, node):
        self.DefaultBehaviour(node)

    def VisitLocalVarDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        self.DefaultBehaviour(node)
