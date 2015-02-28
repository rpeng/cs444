
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
    
    def VisitCompilationUnit(self, node):
        pass

    def VisitPackageDecl(self, node):
        pass

    def VisitImportDecl(self, node):
        pass

    def VisitTypeDecl(self, node):
        pass

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
        for fd in node.field_decls:
            fd.visit(self)
        for md in node.method_decls:
            md.visit(self)
        for cd in node.constructor_decls:
            cd.visit(self)
    
    def VisitMethodDecl(self, node):
        modifiers = [x.lexeme for x in node.header.modifiers]
        if (('abstract' in modifiers or 'native' in modifiers) and
                node.body[0].token.lexeme is not ';'):
            _err(node.modifiers[0],
                 "A method has a body if and"
                 "only if it is neither abstract nor native")
        if node is not None:
            node.body.visit(self)

    def VisitMethodHeader(self, node):
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
            modifiers = [x.lexeme for x in node.method_headers.modifiers]
            if ('static' in modifiers or 'final' in modifiers 
                    or 'native' in modifiers):
                _err(node.modifiers[0],
                 'An interface method cannot be static, final, or native')
    
    def VisitFieldDecl(self, node):
        modifiers = [x.lexeme for x in node.modifiers]
        if 'final' in modifiers and node.var_decl is None:
            _err(node.modifiers[0], "A final field must be initialized")
        if 'public' not in modifiers and 'protected' not in modifiers:
            _err(node.f_type, "Package cannot have private field")
        if node.var_decl:
            node.var_decl.visit(self)
    
    def VisitConstructorDecl(self, node):
        pass
    
    def VisitVariableDecl(self, node):
        pass
    
    def VisitParameter(self, node):
        pass
    
    def VisitType(self, node):
        pass

    def VisitName(self, node):
        pass
    
    ### Statement ###
    def VisitIfThenStatement(self, node):
        pass
    
    def VisitIfThenElseStatement(self, node):
        pass
    
    def VisitWhileStatement(self, node):
        pass
    
    def VisitForStatement(self, node):
        pass
    
    def VisitLocalVarDecl(self, node):
        pass
    

    ### Expression ###
    def VisitLiteral(self, node):
        if node.token.token_type == 'INT' and node.token.lexeme > 2147483647:
            _err(node.l_type, "Integer overflowed")


   
    def VisitExpression(self, node):
        pass



