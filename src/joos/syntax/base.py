from lexer.parser import ParseTreeNode
from structs.cfg import Rule


class AbstractSyntaxNode(object):
    # Abstract
    def __init__(self):
        # Populated by the ast_builder
        self.token = None
        self.rule = None
        self.children = None

        # For environment building
        self.env = None

    def InitializeDefaults(self, node):
        self.token = node.token
        self.rule = node.rule
        self.children = node.children

    def NonDefaultKeys(self):
        default_keys = ['rule', 'token', 'children']
        return [x for x in self.__dict__.keys() if x not in default_keys]

    def StrTree(self, indent=0):
        result = " "*indent
        result += repr(self) + ": " + " ".join(self.NonDefaultKeys())
        result += '\n'
        for key in self.NonDefaultKeys():
            child = self.__dict__[key]
            if isinstance(child, AbstractSyntaxNode):
                result += child.StrTree(indent + 2)
            elif isinstance(child, list):
                result += " "*(indent + 2) + key + " list:" + "\n"
                for node in child:
                    if isinstance(node, AbstractSyntaxNode):
                        result += node.StrTree(indent + 4)
        return result


    def __repr__(self):
        return self.__class__.__name__

    def __getitem__(self, idx):
        return self.children[idx]


class CompilationUnit(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateCompilationUnit(cls, node)

    def visit(self, visitor):
        visitor.VisitCompilationUnit(self)

    def __init__(self, pkg_decl, import_decls, type_decls):
        self.pkg_decl = pkg_decl  # Name
        self.import_decls = import_decls  # Name[]
        self.type_decls = type_decls  # Type[]


class Type(AbstractSyntaxNode):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateType(cls, node)


class ArrayType(Type):
    # int[], Object[]

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayType(cls, node)

    def visit(self, visitor):
        visitor.VisitArrayType(self)

    def __init__(self, type_or_name):
        self.type_or_name = type_or_name  # Type | Name


class ClassOrInterfaceType(Type):
    # class x; interface x;

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassOrInterfaceType(cls, node)

    def visit(self, visitor):
        visitor.VisitClassOrInterfaceType(self)

    def __init__(self, name):
        self.name = name  # token[]


class PrimitiveType(Type):
    # bool, byte, short, int, char

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePrimitiveType(cls, node)

    def visit(self, visitor):
        visitor.VisitPrimitiveType(self)

    def __init__(self, t_type):
        self.t_type = t_type  # token


class Name(AbstractSyntaxNode):
    # a.b.c.d

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateName(cls, node)

    def visit(self, visitor):
        visitor.VisitName(self)

    def __init__(self, name):
        self.name = name  # token[]


class Literal(AbstractSyntaxNode):
    # 1, 'hi', 'a'

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLiteral(cls, node)

    def visit(self, visitor):
        visitor.VisitLiteral(self)

    def __init__(self, token):
        self.token = token  # token
