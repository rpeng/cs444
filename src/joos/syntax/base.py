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

    def IsInitialized(self):
        return (hasattr(self, 'token')
                or hasattr(self, 'rule')
                or hasattr(self, 'children'))

    def NonDefaultKeys(self):
        default_keys = AbstractSyntaxNode().__dict__.keys()
        return [x for x in self.__dict__.keys() if x not in default_keys]

    def ASTChildren(self):
        for key in self.NonDefaultKeys():
            child = self.__dict__[key]
            if isinstance(child, AbstractSyntaxNode):
                yield child
            elif isinstance(child, list):
                for element in child:
                    if isinstance(element, AbstractSyntaxNode):
                        yield element

    def StrTree(self, indent=0):
        result = " " * indent
        result += repr(self) + ": " + " ".join(self.NonDefaultKeys())
        result += '\n'
        for key in self.NonDefaultKeys():
            child = self.__dict__[key]
            if isinstance(child, AbstractSyntaxNode):
                result += child.StrTree(indent + 2)
            elif isinstance(child, list):
                result += " " * (indent + 2) + key + " list:" + "\n"
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
        return visitor.VisitCompilationUnit(self)

    def __init__(self, pkg_decl, import_decls, type_decl):
        self.pkg_decl = pkg_decl  # Name?
        self.import_decls = import_decls  # ImportDecl[]?
        self.type_decl = type_decl  # ClassDecl? | InterfaceDecl?


class Type(AbstractSyntaxNode):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateType(cls, node)


class ReferenceType(Type):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateReferenceType(cls, node)


class ArrayType(ReferenceType):
    # int[], Object[]

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayType(cls, node)

    def visit(self, visitor):
        return visitor.VisitArrayType(self)

    def __init__(self, type_or_name):
        self.type_or_name = type_or_name  # Type | Name


class ClassOrInterfaceType(ReferenceType):
    # class x; interface x;

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassOrInterfaceType(cls, node)

    def visit(self, visitor):
        return visitor.VisitClassOrInterfaceType(self)

    def __init__(self, name):
        self.name = name  # Name


class PrimitiveType(Type):
    # bool, byte, short, int, char

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePrimitiveType(cls, node)

    def visit(self, visitor):
        return visitor.VisitPrimitiveType(self)

    def __init__(self, t_type):
        self.t_type = t_type  # token


class VoidType(Type):
    # void
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateVoidType(cls, node)

    def visit(self, visitor):
        return visitor.VisitVoidType(self)


class Name(AbstractSyntaxNode):
    # a.b.c.d

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateName(cls, node)

    def visit(self, visitor):
        return visitor.VisitName(self)

    def IsSimple(self):
        return len(self.tokens) == 1

    def Prefix(self):
        return '.'.join([x.lexeme for x in self.tokens[:-1]])

    def Last(self):
        return self.tokens[-1].lexeme

    def Split(self):
        return [x.lexeme for x in self.tokens]

    def AsString(self):
        return '.'.join([x.lexeme for x in self.tokens])

    def __init__(self, tokens):
        self.tokens = tokens  # token[]
        self.linked_type = None  # For linking

    def __repr__(self):
        return """Name: {name}, Linked: {type}""".format(
            name=self.AsString(), type=self.linked_type)


class Literal(AbstractSyntaxNode):
    # 1, 'hi', 'a'

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLiteral(cls, node)

    def visit(self, visitor):
        return visitor.VisitLiteral(self)

    def __init__(self, value):
        self.value = value  # token
