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

    def __getitem__(self, idx):
        return self.children[idx]

class CompilationUnit(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateCompilationUnit(cls, node)

    def visit(self, visitor):
        visitor.VisitCompilationUnit(self)

    def __init__(self, pkg_decl, import_decls, type_decls):
        self.pkg_decl = pkg_decl
        self.import_decls = import_decls
        self.type_decls = type_decls

class PackageDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePackageDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitPackageDecl(self)

    def __init__(self, name):
        self.name = name

class ImportDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateImportDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitImportDecl(self)

    def __init__(self, name):
        self.name = name

class TypeDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateTypeDecl(cls, node)

class ClassDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitClassDecl(self)

    def __init__(self, modifiers, name, extends, interfaces, field_decls,
            method_decls, constructor_decls):
        self.modifiers = modifiers
        self.name = name  # token
        self.extends = extends
        self.interfaces = interfaces
        self.field_decls = field_decls
        self.method_decls = method_decls
        self.constructor_decls = constructor_decls

    def __repr__(self):
        return "ClassDecl: '{}'".format(self.name)

class MethodDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitMethodDecl(self)

    def __init__(self, header, body):
        self.header = header
        self.body = body

class MethodHeader(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodHeader(cls, node)

    def visit(self, visitor):
        visitor.VisitMethodHeader(self)

    def __init__(self, modifiers, m_type, m_id, m_param):
        self.modifiers = modifiers
        self.m_type = m_type
        self.m_id = m_id
        self.m_param = m_param

class InterfaceDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitInterfaceDecl(self)

    def __init__(self, name, extends_interface, method_headers):
        self.name = name  # token
        self.extends_interface = extends_interface
        self.method_headers = method_headers

class FieldDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitFieldDecl(self)

    def __init__(self, modifiers, f_type, var_decl):
        self.modifiers = modifiers
        self.f_type = f_type
        self.var_decl = var_decl

class ConstructorDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateConstructorDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitConstructorDecl(self)

    def __init__(self, modifiers, name, params, body):
        self.modifiers = modifiers
        self.name = name
        self.params = params
        self.body = body

class VariableDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateVariableDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitVariableDecl(self)

    def __init__(self, var_id, exp):
        self.var_id = var_id
        self.exp = exp

class Parameter(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateParameter(cls, node)

    def visit(self, visitor):
        visitor.VisitParameter(self)

    def __init__(self, p_type, var_id):
        self.p_type = p_type
        self.var_id = var_id

class Type(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateType(cls, node)

    def visit(self, visitor):
        visitor.VisitType(self)

    def __init__(self, t_type):
        self.t_type = t_type

class PrimitiveType(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePrimitiveType(cls, node)

    def visit(self, visitor):
        visitor.VisitPrimitiveType(self)

    def __init__(self, t_type):
        self.t_type = t_type

class Name(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateName(cls, node)

    def visit(self, visitor):
        visitor.VisitName(self)

    def __init__(self, name):
        self.name = name

class MethodInvocation(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodInvocation(cls, node)

    def visit(self, visitor):
        visitor.VisitMethodInvocation(self)

    def __init__(self, primary, name, args):
        self.primary = primary
        self.name = name
        self.args = args

class Block(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateBlock(cls, node)

    def visit(self, visitor):
        visitor.VisitBlock(self)

    def __init__(self, stmts):
        self.stmts = stmts
