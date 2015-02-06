from compiler.parser import ParseTreeNode
from structs.cfg import Rule


class AbstractSyntax(object):
    def __repr__(self):
        return self.__class__.__name__

    def StrTree(self, indent=0):
        result = " "*indent
        result += str(self.__dict__)
        result += '\n'
        for child in self.children:
            result += child.StrTree(indent + 2)
        return result


class InterfaceMethodDecl(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceMethodDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitInterfaceMethodDecl(self)

    def __init__(self, modifiers, m_type, decl):
        self.modifiers = modifiers
        self.m_type = m_type
        self.decl = decl


class MethodDecl(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitMethodDecl(self)

    def __init__(self, modifiers, m_type, decl, body):
        self.modifiers = modifiers
        self.m_type = m_type
        self.decl = decl
        self.body = body


class InterfaceDecl(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitInterfaceDecl(self)

    def __init__(self, name, extends_interface, body):
        self.name = name  # token
        self.extends_interface = extends_interface
        self.body = body


class ClassDecl(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitClassDecl(self)

    def __init__(self, modifiers, name, extends, interfaces, body):
        self.modifiers = modifiers
        self.name = name  # token
        self.extends = extends
        self.interfaces = interfaces
        self.body = body

    def __repr__(self):
        return "ClassDecl: '{}'".format(self.name)


class Modifiers(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateModifiers(cls, node)

    def visit(self, visitor):
        visitor.VisitModifiers(self)

    def __init__(self, modifiers):
        self.modifiers = modifiers

    def __repr__(self):
        return "Modifiers: '{}'".format(self.modifiers)


class Literal(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLiteral(cls, node)

    def visit(self, visitor):
        visitor.VisitLiteral(self)

    def __init__(self, l_type, value):
        self.l_type = l_type
        self.value = value


class FieldDecl(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitFieldDecl(self)

    def __init__(self, modifiers, decl_type, var_decl):
        self.modifiers = modifiers
        self.decl_type = decl_type
        self.var_decl = var_decl


class ClassMemberDecl(AbstractSyntax):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassMemberDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitClassMemberDecl(self)

    def __init__(self, modifiers, cf_type, decl, body):
        self.modifiers = modifiers
        self.cf_type = cf_type
        self.decl = decl
        self.body = body


rules_map = {
    'ClassDeclaration': ClassDecl,
    'Modifiers': Modifiers,
    'MethodDeclaration': MethodDecl,
    'AbstractMethodDeclaration': InterfaceMethodDecl,
    'InterfaceDeclaration': InterfaceDecl,
    'FieldDeclaration': FieldDecl,
    'Literal': Literal,
    # 'ClassMemberDeclaration': ClassMemberDecl
}
