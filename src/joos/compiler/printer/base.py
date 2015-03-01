from joos.compiler.printer import *
from joos.syntax import ASTVisitor

class ASTPrinter(DeclPrinterMixin, ASTVisitor):
    def __init__(self, indent=0):
        self.indent = indent

    def i(self):
        # Adds an indent
        return " "*self.indent

    def r(self, name):
        # Resolves a name
        if name:
            return ".".join([x.lexeme for x in name])

    def rs(self, names):
        # Joins a list of names
        if names:
            return ", ".join([self.r(x) for x in names])

    def j(self, tokens):
        # Joins a list of tokens
        if tokens:
            return ", ".join([x.lexeme for x in tokens])

    def ns(self, list_to_check, indent_add=4):
        if list_to_check:
            return '\n'.join([ASTPrinter(self.indent+indent_add).Visit(x)
                              for x in list_to_check])
        else:
            return "{i}None".format(i=self.i() + " "*indent_add)

    # Base
    def VisitCompilationUnit(self, node):
        return """{i}CompilationUnit:
{i}  Package Name: {pkg}
{i}  Imports: {imports}
{i}  Type Declarations:
{type_decls}
""".format(i=self.i(),
           pkg=self.r(node.pkg_decl.name),
           imports=self.rs([x.name for x in node.import_decls]),
           type_decls=self.ns(node.type_decls))

    def VisitArrayType(self, node):
        return node.type_or_name.visit(self) + "[]"

    def VisitClassOrInterfaceType(self, node):
        return self.DefaultBehaviour(node)

    def VisitPrimitiveType(self, node):
        return node.t_type.lexeme

    def VisitName(self, node):
        return self.r(node.name)

    def VisitLiteral(self, node):
        return self.DefaultBehaviour(node)
