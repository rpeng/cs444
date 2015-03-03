class DeclPrinterMixin(object):
    # Decl
    def VisitPackageDecl(self, node):
        pass

    def VisitImportDecl(self, node):
        pass

    def VisitClassDecl(self, node):
        return """{i}ClassDeclaration:
{i}  Name: {name}
{i}  Modifiers: {modifiers}
{i}  Extends: {extends}
{i}  Implements: {implements}
{i}  Fields:
{fields}
{i}  Methods:
{methods}
{i}  Constructors:
{cons}
""".format(i=self.i(), name=node.name.lexeme,
           modifiers=self.j(node.modifiers),
           extends=self.r(node.extends),
           implements=self.rs(node.interfaces),
           fields=self.ns(node.field_decls),
           methods=self.ns(node.method_decls),
           cons=self.ns(node.constructor_decls))

    def VisitInterfaceDecl(self, node):
        return """{i}InterfaceDeclaration:
{i}  Name: {name}
{i}  Extends: {extends}
{i}  Methods:
{methods}
""".format(i=self.i(), name=node.name.lexeme,
           extends=self.rs(node.extends_interface),
           methods=self.ns(node.method_decls))

    def VisitMethodDecl(self, node):
        return """{i}Method:
{header}
{body}
""".format(i=self.i(), header=self.n(node.header, 2),
           body=self.n(node.body_block, 2))

    def VisitMethodHeader(self, node):
        return """{i}Header:
{i}  Modifiers: {modifiers}
{i}  Type: {m_type}
{i}  ID: {m_id}
{i}  Parameters:
{parameters}
""".format(i=self.i(), modifiers=self.j(node.modifiers),
           m_type=node.m_type.visit(self),
           m_id=node.m_id.lexeme,
           parameters=self.ns(node.params))

    def VisitFieldDecl(self, node):
        return """{i}FieldDeclaration:
{i}  Modifiers: {modifiers}
{i}  Type: {type}
{i}  Variable Declaration:
{vardecl}
""".format(i=self.i(),
           modifiers=self.j(node.modifiers),
           vardecl=self.n(node.var_decl),
           type=node.f_type.visit(self))

    def VisitConstructorDecl(self, node):
        return """{i}ConstructorDeclaration:
{i}  Modifiers: {modifiers}
{i}  Name: {name}
{i}  Parameters:
{params}
{i}  Body: {body}
""".format(i=self.i(), modifiers=self.j(node.modifiers),
           name=node.name.lexeme, params=self.ns(node.params),
           body=self.n(node.body))

    def VisitVariableDeclarator(self, node):
        return """{i}Variable {x}:
{e}
""".format(i=self.i(), x=node.var_id.lexeme, e=self.n(node.exp, 2))

    def VisitLocalVarDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        return "{i}{type} {name}".format(
            i=self.i(),
            type=node.p_type.visit(self),
            name=node.var_id.lexeme)
