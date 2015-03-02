from joos.syntax import *


def _err(token, msg):
    string = "Row {} col {}: {}".format(token.row, token.col, msg)
    raise RuntimeError(string)


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

    def _CheckModifiersCommon(self, modifiers):
        # Check duplicate
        hashed = set()
        for modifier in modifiers:
            if modifier.lexeme in hashed:
                _err(modifier, "Duplicate modifier: " + modifier.lexeme)
            hashed.add(modifier.lexeme)

    def VisitClassDecl(self, node):
        self._CheckModifiersCommon(node.modifiers)

        modifiers = [x.lexeme for x in node.modifiers]
        if node.name.lexeme != self.filename:
            _err(node.name, "The class name must match the filename "
                 + self.filename)
        if 'abstract' in modifiers and 'final' in modifiers:
            _err(node.modifiers[0],
                 "A class cannot be both abstract and final")
        if 'public' not in modifiers and 'protected' not in modifiers:
            _err("Class cannot be private")
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
            _err(node.header.modifiers[0],
                 "A method has a body if and"
                 "only if it is neither abstract nor native")
        if node.body_block is not None and node.body_block.stmts is not None:
            for stmt in node.body_block.stmts:
                stmt.visit(self)

    def VisitMethodHeader(self, node):
        self._CheckModifiersCommon(node.modifiers)

        modifiers = [x.lexeme for x in node.modifiers]
        if 'abstract' in modifiers and ('static' in modifiers
                                        or 'final' in modifiers):
            _err(node.modifiers[0],
                 'An abstract method cannot be static or final')
        if 'static' in modifiers and 'final' in modifiers:
            _err(node.modifiers[0], 'A static method cannot be final')
        if 'native' in modifiers and 'static' not in modifiers:
            _err(node.modifiers[0], 'A native method must be static')
        if 'public' not in modifiers and 'protected' not in modifiers:
            _err("Package cannot have private field")

    def VisitInterfaceDecl(self, node):
        if node.name.lexeme != self.filename:
            _err(node.name, "The interface name must match the filename "
                 + self.filename)
        if node.method_headers:
            for header in node.method_headers:
                modifiers = [x.lexeme for x in header.modifiers]
                if ('static' in modifiers or 'final' in modifiers
                        or 'native' in modifiers):
                    _err(header.modifiers[0],
                         ('An interface method cannot be '
                          'static, final, or native'))
                header.visit(self)

    def VisitFieldDecl(self, node):
        self._CheckModifiersCommon(node.modifiers)

        modifiers = [x.lexeme for x in node.modifiers]
        if 'final' in modifiers and node.var_decl.exp is None:
            _err(node.modifiers[0], "A final field must be initialized")
        if 'public' not in modifiers and 'protected' not in modifiers:
            _err(node.f_type, "Package cannot have private field")
        if node.var_decl:
            node.var_decl.visit(self)

    # Expression
    def VisitLiteral(self, node):
        if (node.value.token_type == 'INT'
                and int(node.value.lexeme) > 2147483647):
            _err(node.value, "Integer overflowed")

    def VisitCastExpression(self, node):
        if not (isinstance(node.cast_type, PrimitiveType) or
                isinstance(node.cast_type, ClassOrInterfaceType) or
                isinstance(node.cast_type, Name) or
                isinstance(node.cast_type, ArrayType)):
            _err(node[0].token,
                 "A cast must be of primitive or reference types")

    def VisitConstructorDecl(self, node):
        self._CheckModifiersCommon(node.modifiers)

        if node.name.lexeme != self.filename:
            _err(node.name, "Constructor must have same name as base class")

        if node.body:
            node.body.visit(self)
