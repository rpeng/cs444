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


class ClassDecl(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassDecl(cls, node)

    def __init__(self, modifiers, name, body):
        self.modifiers = modifiers
        self.name = name
        self.body = body

    def __repr__(self):
        return "ClassDecl: '{}'".format(self.name)


class Modifiers(object):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateModifiers(cls, node)

    def __init__(self, modifiers):
        self.modifiers = modifiers

    def __repr__(self):
        return "Modifiers: '{}'".format(self.modifiers)


rules_map = {
    'ClassDeclaration': ClassDecl,
    'Modifiers': Modifiers
}
