from compiler.parser import ParseTreeNode
from structs.cfg import Rule


class AbstractSyntaxNode(object):
    def __repr__(self):
        return self.__class__.__name__

    def StrTree(self, indent=0):
        result = " "*indent
        result += str(self.__dict__)
        result += '\n'
        for child in self.children:
            result += child.StrTree(indent + 2)
        return result


class InterfaceMemberDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceMethodDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitInterfaceMemberDecl(self)

    def __init__(self, modifiers, m_type, decl):
        self.modifiers = modifiers
        self.m_type = m_type
        self.decl = decl


class MethodDecl(AbstractSyntaxNode):
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

class Name(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateName(cls, node)

    def visit(self, visitor):
        visitor.VisitName(self)

    def __init__(self, name):
        self.name = name

class InterfaceDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitInterfaceDecl(self)

    def __init__(self, name, extends_interface, body):
        self.name = name  # token
        self.extends_interface = extends_interface
        self.body = body


class ClassDecl(AbstractSyntaxNode):
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


class Literal(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLiteral(cls, node)

    def visit(self, visitor):
        visitor.VisitLiteral(self)

    def __init__(self, l_type, value):
        self.l_type = l_type
        self.value = value


class FieldDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitFieldDecl(self)

    def __init__(self, modifiers, decl_type, var_decl):
        self.modifiers = modifiers
        self.decl_type = decl_type
        self.var_decl = var_decl


class ClassMemberDecl(AbstractSyntaxNode):
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
    'MethodDeclaration': MethodDecl,
    'InterfaceMemberDeclaration': InterfaceMemberDecl,
    'InterfaceDeclaration': InterfaceDecl,
    'FieldDeclaration': FieldDecl,
    'Literal': Literal,
    'Name': Name
    # 'ClassMemberDeclaration': ClassMemberDecl
}
