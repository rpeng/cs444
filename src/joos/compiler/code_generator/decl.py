from joos.compiler.code_generator.tools.vars import Vars
from structs.utils import memoize


NATIVE_WRITE = "NATIVEjava.io.OutputStream.nativeWrite"

class DeclCodeMixin(object):

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
        for decl in node.ordered_methods.values():
            if not decl.IsStatic():
                decl_name = self.namer.Visit(decl)
                self.symbols.Import(decl_name)
                self.writer.OutputLine("dd {}".format(decl_name))

        self.writer.Dedent()

    def OutputStaticInitializer(self, node):
        class_name = self.namer.Visit(node)
        self.writer.OutputLine("; Static initializer")
        self.symbols.DefineSymbolLabel("is~{}".format(class_name))
        with self.writer.FunctionContext():
            if node.field_decls:
                for decl in node.field_decls:
                    if decl.IsStatic():
                        self.VisitFieldDecl(decl)

    def OutputFieldInitializer(self, node):
        class_name = self.namer.Visit(node)
        field_label = "if~{}".format(class_name)

        self.writer.OutputLine("; Field initializer")
        self.symbols.DefineSymbolLabel(field_label)
        self.writer.Indent()

        if node.extends is not None: # call parent field initializer
            parent_initializer = "if~{}".format(
                self.namer.Visit(node.extends.linked_type))
            self.symbols.Import(parent_initializer)
            self.writer.OutputLine("; parent field initializer")
            self.writer.OutputLine("push eax")
            self.writer.OutputLine("call {}".format(parent_initializer))
            self.writer.OutputLine("add esp, 4")

        self.writer.OutputLine("; own fields")
        with self.writer.FunctionContext(0):
            if node.field_decls:
                for decl in node.field_decls:
                    if not decl.IsStatic():
                        self.VisitFieldDecl(decl)

        self.writer.Dedent()

    def OutputInstanceCreator(self, node):
        class_name = self.namer.Visit(node)
        creator_label = "new~{}".format(class_name)
        required_size = len(node.ordered_fields) * 4 + 4

        self.writer.OutputLine("; Instance creator")
        self.symbols.DefineSymbolLabel(creator_label)
        self.writer.Indent()

        with self.writer.FunctionContext():
            self.writer.OutputLine('push ecx')
            self.writer.OutputLine('push edx')

            self.symbols.Import("__malloc")
            self.writer.OutputLine("mov eax, {}".format(required_size))
            self.writer.OutputLine("call __malloc")

            # Copy in vtable
            self.writer.OutputLine("mov [eax], dword V~{}".format(class_name))
            # Call field initializer
            self.writer.OutputLine("push eax")
            self.writer.OutputLine("call if~{}".format(class_name))
            self.writer.OutputLine("pop eax")

            self.writer.OutputLine('pop ecx')
            self.writer.OutputLine('pop edx')

        self.writer.Dedent()

    def VisitPackageDecl(self, node):
        pass

    def VisitImportDecl(self, node):
        pass

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
                    self.symbols.Export(field_name)
                    self.writer.OutputLine(field_name + ' resd 1')
        self.writer.OutputLine("")

        # .text
        self.writer.OutputLine("section .text")
        self.writer.OutputLine("; Methods")
        self.Visit(node.constructor_decls)
        self.Visit(node.method_decls)

        self.OutputStaticInitializer(node)
        self.OutputFieldInitializer(node)
        self.OutputInstanceCreator(node)

        # imports
        self.symbols.GenerateSymbolsSection()

    def VisitInterfaceDecl(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        # link the methods globally
        method_name = self.namer.Visit(node)
        self.symbols.DefineSymbolLabel(method_name)
        with self.writer.FunctionContext():
            self.vars.SetParams(node.header.params, node.IsStatic())
            if node.IsNative():
                self.symbols.Import(NATIVE_WRITE)
                self.writer.OutputLine("; native output")
                self.writer.OutputLine("mov eax, [ebp + 8]")
                self.writer.OutputLine("push ecx")
                self.writer.OutputLine("push edx")
                self.writer.OutputLine("call {}".format(NATIVE_WRITE))
                self.writer.OutputLine("pop edx")
                self.writer.OutputLine("pop ecx")
            else:
                self.Visit(node.body_block)

    def VisitMethodHeader(self, node):
        self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        # For its initializer
        type_decl = node.env.LookupClassOrInterface()[1]
        self.writer.OutputLine('; initializer for field {}'.format(
            node.var_decl.var_id.lexeme))
        if node.IsStatic():
            location = self.namer.Visit(node)
        else:
            offset = Vars.GetFieldOffset(node)
            self.writer.OutputLine('mov ecx, [ebp + 8]')
            self.writer.OutputLine('add ecx, {}'.format(offset))
            location = 'ecx'
        if node.var_decl.exp is not None:
            self.Visit(node.var_decl)
            self.writer.OutputLine('mov [{}], eax'.format(location))
        else:
            self.writer.OutputLine('mov [{}], dword 0'.format(location))

    def VisitConstructorDecl(self, node):
        # link the methods globally
        constructor_name = self.namer.Visit(node)
        self.symbols.DefineSymbolLabel(constructor_name)
        with self.writer.FunctionContext():
            self.writer.OutputLine('; constructor body')
            self.vars.SetParams(node.params, False)
            self.Visit(node.body)

    def VisitVariableDeclarator(self, node):
        if node.exp is not None:
            self.Visit(node.exp)
        else:
            self.writer.OutputLine('move eax, 0')

    def VisitLocalVarDecl(self, node):
        self.Visit(node.var_decl)
        self.vars.AddLocalVar(node)

    def VisitParameter(self, node):
        self.DefaultBehaviour(node)
