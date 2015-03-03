from joos.compiler.printer import *
from joos.syntax import ASTVisitor


class ASTPrinter(DeclPrinterMixin, StmtPrinterMixin,
                 ExprPrinterMixin, ASTVisitor):
    def __init__(self, indent=0):
        self.indent = indent

    def i(self):
        # Adds an indent
        return " " * self.indent

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

    def n(self, node, indent_add=4):
        # Resolves an AST node
        if node:
            return ASTPrinter(self.indent + indent_add).Visit(node)
        else:
            return "{i}None".format(i=self.i() + " " * indent_add)

    def ns(self, list_to_check, indent_add=4):
        # Resolves a list of AST nodes
        if list_to_check:
            return '\n'.join([ASTPrinter(self.indent + indent_add).Visit(x)
                              for x in list_to_check])
        else:
            return "{i}None".format(i=self.i() + " " * indent_add)

    def DefaultBehaviour(self, node):
        return "{i} {node} NOT IMPLEMENTED".format(i=self.i(), node=node)

    # Base
    def VisitCompilationUnit(self, node):
        pkg = None
        imports = None
        if node.pkg_decl:
            pkg = self.j(node.pkg_decl.name)
        if node.import_decls:
            imports = self.rs([x.name for x in node.import_decls])
        return """{i}CompilationUnit:
{i}  Package Name: {pkg}
{i}  Imports: {imports}
{i}  Type Declaration:
{type_decl}
""".format(i=self.i(),
           pkg=pkg,
           imports=imports,
           type_decl=self.n(node.type_decl))

    def VisitArrayType(self, node):
        return node.type_or_name.visit(self) + "[]"

    def VisitClassOrInterfaceType(self, node):
        return self.r(node.name)

    def VisitVoidType(self, node):
        return 'void'

    def VisitPrimitiveType(self, node):
        return node.t_type.lexeme

    def VisitName(self, node):
        return self.r(node.name)

    def VisitLiteral(self, node):
        return """{i}Literal: {value}""".format(i=self.i(),
                                                value=node.value.lexeme)
