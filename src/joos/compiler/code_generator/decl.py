class DeclCodeMixin(object):
    def VisitPackageDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitImportDecl(self, node):
        self.DefaultBehaviour(node)

    def OutputVtable(self, node):
        class_name = self.namer.Visit(node)
        self.writer.OutputLine("; VTable")
        self.symbols.DefineSymbolLabel("V~{}".format(class_name))
        self.writer.Indent()

        self.writer.OutputLine("dd n~{}".format(class_name))
        if node.extends:
            super_name = self.namer.Visit(node.extends.linked_type)
            v_name = "V~{}".format(super_name)
            self.symbols.Import(v_name)
            self.writer.OutputLine("dd {}".format(v_name))
        else:
            self.writer.OutputLine("dd 0")

        self.writer.OutputLine("; methods")
        for decl in node.method_map.values():
            if not decl.IsStatic():
                decl_name = self.namer.Visit(decl)
                self.symbols.Import(decl_name)
                self.writer.OutputLine("dd {}".format(decl_name))

        self.writer.Dedent()

    def OutputStaticInitializer(self, node):
        class_name = self.namer.Visit(node)
        # Static initializer
        self.writer.OutputLine("; Static initializer")
        self.symbols.DefineSymbolLabel("is~{}".format(class_name))
        with self.writer.FunctionContext():
            if node.field_decls:
                for decl in node.field_decls:
                    if decl.IsStatic():
                        self.VisitFieldDecl(decl)

    def VisitClassDecl(self, node):
        class_name = self.namer.Visit(node)

        # .data
        # v-table
        self.writer.OutputLine("section .data")
        self.OutputVtable(node)
        self.writer.OutputLine("")

        # class name
        self.symbols.DefineSymbolLabel("n~{}".format(class_name))
        self.writer.Indent()
        self.writer.OutputLine("db {}, \"{}\"".format(len(class_name), class_name))
        self.writer.Dedent()
        self.writer.OutputLine("")

        self.writer.OutputLine("section .bss")
        self.writer.OutputLine("; Static decls")
        if node.field_decls:
            for decl in node.field_decls:
                if decl.IsStatic():
                    field_name = self.namer.Visit(decl)
                    self.writer.OutputLine(field_name + ' resd 1')
        self.writer.OutputLine("")

        # .text
        self.writer.OutputLine("section .text")
        self.writer.OutputLine("; Methods")
        self.Visit(node.constructor_decls)
        self.Visit(node.method_decls)

        self.OutputStaticInitializer(node)

        # imports
        self.symbols.GenerateSymbolsSection()

    def VisitInterfaceDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        # link the methods globally
        method_name = self.namer.Visit(node)
        self.symbols.DefineSymbolLabel(method_name)
        with self.writer.FunctionContext():
            self.writer.OutputLine('; method body')
            #TODO self.Visit(node.body_block)

    def VisitMethodHeader(self, node):
        self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        # For its initializer
        if node.IsStatic():
            self.writer.OutputLine('; initializer for field {}'.format(
                node.var_decl.var_id.lexeme))
            location = self.namer.Visit(node)
            if node.var_decl.exp is not None:
                self.Visit(node.var_decl.exp)
                self.writer.OutputLine('mov [{}], eax'.format(location))
            else:
                self.writer.OutputLine('mov [{}], dword 0'.format(location))
        else:
            self.DefaultBehaviour(node)

    def VisitConstructorDecl(self, node):
        # link the methods globally
        constructor_name = self.namer.Visit(node)
        self.symbols.DefineSymbolLabel(constructor_name)
        with self.writer.FunctionContext():
            self.writer.OutputLine('; constructor body')
            #TODO self.Visit(node.body)

    def VisitVariableDeclarator(self, node):
        self.Visit(node.exp)

    def VisitLocalVarDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        self.DefaultBehaviour(node)
