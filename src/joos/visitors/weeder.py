
def _err(token, msg):
    string = "Row {} col {}: {}".format(token.row, token.col, msg)
    raise RuntimeError(string)


class WeederVisitor(object):
    def __init__(self, filename):
        self.filename = filename.split('/')[-1][:-5]

    def VisitParseTreeNode(self, node):
        for child in node.children:
            if child:
                child.visit(self)

    def VisitMethodDecl(self, node):
        modifiers = [x.lexeme for x in node.modifiers]
        if (('abstract' in modifiers or 'native' in modifiers) and
                node.body is not None):
            _err(node.modifiers[0],
                 "A method has a body if and"
                 "only if it is neither abstract nor native")
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
        if node is not None:
            node.body.visit(self)

    def VisitLiteral(self, node):
        if node.l_type.token_type == 'INT' and node.value > 2147483647:
            _err(node.l_type, "Integer overflowed")

    def VisitInterfaceDecl(self, node):
        if node.name.lexeme != self.filename:
            _err(node.name, "The interface name must match the filename "
                 + self.filename)
        node.body.visit(self)

    def VisitInterfaceMethodDecl(self, node):
        modifiers = [x.lexeme for x in node.modifiers]
        if ('static' in modifiers or 'final' in modifiers
                or 'native' in modifiers):
            _err(node.modifiers[0],
                 'An interface method cannot be static, final, or native')

    def VisitFieldDecl(self, node):
        modifiers = [x.lexeme for x in node.modifiers]
        if 'final' in modifiers and node.var_decl is None:
            _err(node.modifiers[0], "A final field must be initialized")
        if 'public' not in modifiers and 'protected' not in modifiers:
            _err(node.decl_type, "Package cannot have private field")
        if node.decl_type:
            node.decl_type.visit(self)
        if node.var_decl:
            node.var_decl.visit(self)

    def VisitClassDecl(self, node):
        modifiers = [x.lexeme for x in node.modifiers]
        if node.name.lexeme != self.filename:
            _err(node.name, "The class name must match the filename "
                 + self.filename)
        if 'abstract' in modifiers and 'final' in modifiers:
            _err(node.modifiers[0],
                 "A class cannot be both abstract and final")
        if 'public' not in modifiers and 'protected' not in modifiers:
            _err("Class cannot be private")
        if node.extends:
            node.extends.visit(self)
        if node.interfaces:
            node.interfaces.visit(self)
        if node.body:
            node.body.visit(self)

    def VisitModifiers(self, node):
        pass
