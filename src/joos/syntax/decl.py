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
        self.name = name  # Name -> Type
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

    def IsAbstract(self):
        modifiers = [x.lexeme for x in self.modifiers]
        return 'abstract' in modifiers

    def NonDefaultKeys(self):
        return ['extends', 'interfaces', 'field_decls', 'method_decls',
                'constructor_decls']

    def __init__(self, modifiers, name, extends, interfaces, field_decls,
                 method_decls, constructor_decls):
        self.modifiers = modifiers  # token[]
        self.name = name  # token
        self.extends = extends  # Name?
        self.interfaces = interfaces  # Name[]?
        self.field_decls = field_decls  # FieldDecl[]?
        self.method_decls = method_decls  # MethodDecl[]?
        self.constructor_decls = constructor_decls  # ConstructorDecl[]

        # linked
        self.ordered_fields = None  # All non-static fields of this class
        self.ordered_methods = None  # All non-static methods in order
        self.linked_interfaces = set()
        self.linked_supers = []
        self.method_map = {}  # Methods [sig -> decl]
        self.cons_map = {}  # Constructors [sig -> decl]
    def __str__(self):
        return self.name.lexeme

class InterfaceDecl(TypeDecl):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInterfaceDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitInterfaceDecl(self)

    def NonDefaultKeys(self):
        return ['name', 'extends_interface', 'method_decls']

    def __init__(self, name, extends_interface, method_decls):
        self.name = name  # token
        self.extends_interface = extends_interface  # Name[]?
        self.method_decls = method_decls  # MethodDecls[]?

        # linked
        self.linked_interfaces = set()
        self.method_map = {}


class MethodDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitMethodDecl(self)

    def IsAbstract(self):
        return self.body_block is None and 'native' not in self.modifiers

    def IsStatic(self):
        return 'static' in self.modifiers

    def IsProtected(self):
        return 'protected' in self.modifiers

    def IsNative(self):
        return 'native' in self.modifiers

    def __init__(self, header, body_block):
        self.header = header  # MethodHeader
        self.body_block = body_block  # Block?
        self.modifiers = [x.lexeme for x in self.header.modifiers]


class MethodHeader(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodHeader(cls, node)

    def visit(self, visitor):
        return visitor.VisitMethodHeader(self)

    def __init__(self, modifiers, m_type, m_id, params):
        self.modifiers = modifiers  # token[]
        self.m_type = m_type  # Type
        self.m_id = m_id  # token
        self.params = params  # Parameter[]?


class FieldDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitFieldDecl(self)

    def IsStatic(self):
        modifiers = [x.lexeme for x in self.modifiers]
        return 'static' in modifiers

    def IsProtected(self):
        modifiers = [x.lexeme for x in self.modifiers]
        return 'protected' in modifiers

    def __init__(self, modifiers, f_type, var_decl):
        self.modifiers = modifiers  # token[]
        self.f_type = f_type  # Type
        self.var_decl = var_decl  # VariableDeclarator


class ConstructorDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateConstructorDecl(cls, node)

    def visit(self, visitor):
        return visitor.VisitConstructorDecl(self)

    def IsProtected(self):
        modifiers = [x.lexeme for x in self.modifiers]
        return 'protected' in modifiers


    def __init__(self, modifiers, name, params, body):
        self.modifiers = modifiers  # token[]
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
