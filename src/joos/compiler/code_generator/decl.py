class DeclCodeMixin(object):
    def VisitPackageDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitImportDecl(self, node):
        self.DefaultBehaviour(node)

    def OutputVtable(self, node):
        class_name = self.namer.Visit(node)
        self.writer.OutputLine("; VTable")
        self.writer.DefineGlobalLabel("V~{}".format(class_name))
        self.writer.Indent()

        self.writer.OutputLine("dd n~{}".format(class_name))
        if node.extends:
            # TODO: request import
            self.writer.OutputLine("dd V~{}".format(node.extends.linked_type))
        else:
            self.writer.OutputLine("dd 0")

        self.writer.OutputLine("; methods")
        for decl in node.method_map.values():
            self.writer.OutputLine("dd {}".format(self.namer.Visit(decl)))

        self.writer.Dedent()

    def VisitClassDecl(self, node):
        class_name = self.namer.Visit(node)

        # .data
        # v-table
        self.writer.OutputLine("section .data")
        self.OutputVtable(node)
        self.writer.OutputLine("")

        # class name
        self.writer.DefineGlobalLabel("n~{}".format(class_name))
        self.writer.Indent()
        self.writer.OutputLine("db {}, \"{}\"".format(len(class_name), class_name))
        self.writer.Dedent()
        self.writer.OutputLine("")

        self.writer.OutputLine("section .bss")
        self.writer.OutputLine("; Statics")
        self.writer.OutputLine("")

        # .text
        self.writer.OutputLine("section .text")
        self.writer.OutputLine("; Methods")
        self.Visit(node.constructor_decls)
        self.Visit(node.method_decls)
        self.writer.OutputLine("")

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
