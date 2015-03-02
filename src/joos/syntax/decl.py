from joos.syntax import AbstractSyntaxNode


class PackageDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePackageDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitPackageDecl(self)

    def __init__(self, name):
        self.name = name  # Name


class ImportDecl(AbstractSyntaxNode):
    CLASS_IMPORT = 0
    PACKAGE_IMPORT = 1

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateImportDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitImportDecl(self)

    def __init__(self, name, import_type):
        self.name = name  # Name
        self.import_type = import_type  # CLASS / PACKAGE


class TypeDecl(AbstractSyntaxNode):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateTypeDecl(cls, node)


class ClassDecl(TypeDecl):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitClassDecl(self)

    def __init__(self, modifiers, name, extends, interfaces, field_decls,
                 method_decls, constructor_decls):
        self.modifiers = modifiers  # token[]?
        self.name = name  # token
        self.extends = extends  # Name?
        self.interfaces = interfaces  # Name[]?
        self.field_decls = field_decls  # FieldDecl[]?
        self.method_decls = method_decls  # MethodDecl[]?
        self.constructor_decls = constructor_decls  # ConstructorDecl[]?


class InterfaceDecl(TypeDecl):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitInterfaceDecl(self)

    def __init__(self, name, extends_interface, method_headers):
        self.name = name  # token
        self.extends_interface = extends_interface  # Name[]?
        self.method_headers = method_headers  # MethodHeader[]?


class MethodDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitMethodDecl(self)

    def __init__(self, header, body_block):
        self.header = header  # MethodHeader
        self.body_block = body_block  # Block?


class MethodHeader(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodHeader(cls, node)

    def visit(self, visitor):
        return visitor.VisitMethodHeader(self)

    def __init__(self, modifiers, m_type, m_id, params):
        self.modifiers = modifiers  # token[]?
        self.m_type = m_type  # Type
        self.m_id = m_id  # token
        self.params = params  # Parameter[]?


class FieldDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitFieldDecl(self)

    def __init__(self, modifiers, f_type, var_decl):
        self.modifiers = modifiers  # token[]?
        self.f_type = f_type  # Type
        self.var_decl = var_decl  # VariableDeclarator


class ConstructorDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateConstructorDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitConstructorDecl(self)

    def __init__(self, modifiers, name, params, body):
        self.modifiers = modifiers  # token[]?
        self.name = name  # token
        self.params = params  # Parameter[]?
        self.body = body  # Block?


class VariableDeclarator(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateVariableDeclarator(cls, node)

    def visit(self, visitor):
        return visitor.VisitVariableDeclarator(self)

    def __init__(self, var_id, exp):
        self.var_id = var_id  # token
        self.exp = exp  # Expression?


class LocalVarDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLocalVarDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitLocalVarDecl(self)

    def __init__(self, l_type, var_decl):
        self.l_type = l_type  # Type
        self.var_decl = var_decl  # VariableDeclarator


class Parameter(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateParameter(cls, node)

    def visit(self, visitor):
        return visitor.VisitParameter(self)

    def __init__(self, p_type, var_id):
        self.p_type = p_type  # Type
        self.var_id = var_id  # token
