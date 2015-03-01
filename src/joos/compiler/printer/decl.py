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
""".format(i=self.i(), name=node.name.lexeme,
           modifiers=self.j(node.modifiers),
           extends=self.r(node.extends),
           implements=self.rs(node.interfaces),
           fields=self.ns(node.field_decls))


    def VisitInterfaceDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodHeader(self, node):
        return self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        return """{i}FieldDeclaration:
{i}  Modifiers: {modifiers}
{i}  Type: {type}
{i}  Variable declaration: {vardecl}""".format(
    i=self.i(), modifiers=self.j(node.modifiers),
    vardecl=node.var_decl.var_id.lexeme,
    type=node.f_type.visit(self))

    def VisitConstructorDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitVariableDeclarator(self, node):
        return self.DefaultBehaviour(node)

    def VisitLocalVarDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        return self.DefaultBehaviour(node)
