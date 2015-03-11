from .common import *
from .classes import CheckClass
from .interfaces import CheckInterface
from joos.syntax import *


def CheckNode(node):
    if node.type_decl:
        if isinstance(node.type_decl, ClassDecl):
            CheckClass(node.type_decl)
        else:
            CheckInterface(node.type_decl)


def CheckHierarchy(app):
    PopulateObject(app)
    for node in app.compilation_units:
        CheckNode(node)
