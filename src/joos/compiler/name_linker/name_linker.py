from joos.compiler.name_linker.disambiguator import Disambiguator
from joos.errors import err
from joos.syntax import ASTVisitor


class NameLinker(ASTVisitor):
    """ Abstract visitor class that visits a parse tree node """
    EXPR_NAME = 0
    TYPE_NAME = 1
    PKG_NAME = 2

    def __init__(self, compilation_unit, type_map):
        self.compilation_unit = compilation_unit
        self.linker = Disambiguator(type_map)
        self.decl = None

    def Start(self):
        self.compilation_unit.visit(self)

    def DefaultBehaviour(self, node):
        for child in node.ASTChildren():
            child.visit(self)

    def VisitPackageDecl(self, node):
        pass

    def VisitMethodInvocation(self, node):
        pass

    def VisitFieldAccess(self, node):
        pass

    # Base
    def Visit(self, node):  # Entry point
        return node.visit(self)

    def VisitFieldDecl(self, node):
        self.decl = node.env.FieldIndex(node.var_decl.var_id.lexeme)
        node.var_decl.visit(self)
        self.decl = None

    def VisitName(self, node):
        if not node.linked_type:
            if self.decl is not None:
                index = node.env.FieldIndex(node.AsString)
                if index is not None and index >= self.decl:
                    err(node.tokens[0], "Invalid forward reference: " + node.AsString())
            self.linker.DisambiguateAndLink(node)
