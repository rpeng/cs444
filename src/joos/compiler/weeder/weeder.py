from joos.errors import err
from joos.syntax import *


class WeederVisitor(ASTVisitor):
    def __init__(self, filename):
        self.filename = filename.split('/')[-1][:-5]

    def VisitParseTreeNode(self, node):
        for child in node.children:
            if child:
                child.visit(self)

    def DefaultBehaviour(self, node):
        for child in node.ASTChildren():
            child.visit(self)

    def _CheckModifiersCommon(self, name, modifiers):
        # Check duplicate
        hashed = set()
        for modifier in modifiers:
            if modifier.lexeme in hashed:
                err(modifier, "Duplicate modifier: " + modifier.lexeme)
            hashed.add(modifier.lexeme)
        modifiers = [x.lexeme for x in modifiers]
        # Check no package private
        if ('public' not in modifiers
                and 'protected' not in modifiers
                and 'private' not in modifiers):
            err(name, "Cannot have package private modifiers")

    def VisitClassDecl(self, node):
        self._CheckModifiersCommon(node.name, node.modifiers)
        modifiers = [x.lexeme for x in node.modifiers]
        if node.name.lexeme != self.filename:
            err(node.name, "The class name must match the filename "
                + self.filename)
        if 'static' in modifiers:
            err(node.modifiers[0], "A class cannot be static")
        if 'native' in modifiers:
            err(node.modifiers[0], "A class cannot be native")
        if 'abstract' in modifiers and 'final' in modifiers:
            err(node.modifiers[0],
                "A class cannot be both abstract and final")
        if 'public' not in modifiers and 'protected' not in modifiers:
            err("Class cannot be private")
        for fd in node.field_decls:
            fd.visit(self)
        for md in node.method_decls:
            md.visit(self)
        for cd in node.constructor_decls:
            cd.visit(self)

    def VisitMethodDecl(self, node):
        node.header.visit(self)

        modifiers = [x.lexeme for x in node.header.modifiers]
        if (('abstract' in modifiers or 'native' in modifiers) and
                node.body_block is not None):
            err(node.header.modifiers[0],
                "A method has a body if and"
                "only if it is neither abstract nor native")
        if node.body_block is not None and node.body_block.stmts is not None:
            for stmt in node.body_block.stmts:
                stmt.visit(self)

    def VisitMethodHeader(self, node):
        self._CheckModifiersCommon(node.m_id, node.modifiers)

        modifiers = [x.lexeme for x in node.modifiers]
        if 'abstract' in modifiers and ('static' in modifiers
                                        or 'final' in modifiers):
            err(node.modifiers[0],
                'An abstract method cannot be static or final')
        if 'static' in modifiers and 'final' in modifiers:
            err(node.modifiers[0], 'A static method cannot be final')
        if 'native' in modifiers and 'static' not in modifiers:
            err(node.modifiers[0], 'A native method must be static')
        if 'public' not in modifiers and 'protected' not in modifiers:
            err("Package cannot have private field")

    def VisitInterfaceDecl(self, node):
        if node.name.lexeme != self.filename:
            err(node.name, "The interface name must match the filename "
                + self.filename)
        if node.method_decls:
            for decl in node.method_decls:
                modifiers = [x.lexeme for x in decl.header.modifiers]
                if ('static' in modifiers or 'final' in modifiers
                        or 'native' in modifiers):
                    err(decl.header.modifiers[0],
                        ('An interface method cannot be '
                         'static, final, or native'))
                decl.header.visit(self)

    def VisitFieldDecl(self, node):
        self._CheckModifiersCommon(node.f_type, node.modifiers)

        modifiers = [x.lexeme for x in node.modifiers]
        if 'final' in modifiers and node.var_decl.exp is None:
            err(node.modifiers[0], "A final field must be initialized")
        if 'public' not in modifiers and 'protected' not in modifiers:
            err(node.f_type, "Package cannot have private field")
        if node.var_decl:
            node.var_decl.visit(self)

    # Expression
    def VisitLiteral(self, node):
        if (node.value.token_type == 'INT'
                and int(node.value.lexeme) > 2147483647):
            err(node.value, "Integer overflowed")

    def VisitCastExpression(self, node):
        if not (isinstance(node.cast_type, PrimitiveType) or
                isinstance(node.cast_type, ClassOrInterfaceType) or
                isinstance(node.cast_type, NameExpression) or
                node.is_array):
            err(node[0].token,
                "A cast must be of primitive or reference types")

    def VisitConstructorDecl(self, node):
        self._CheckModifiersCommon(node.name, node.modifiers)

        if node.name.lexeme != self.filename:
            err(node.name, "Constructor must have same name as base class")

        if node.body:
            node.body.visit(self)

    def VisitLocalVarDecl(self, node):
        if not node.var_decl.exp:
            err(node.name, "Local variable declarations must be initialized.")
