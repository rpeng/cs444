from expr import *
from stmt import *
from decl import *
from base import *


def PrintAST(ast):
    printer = ASTPrinter()
    return printer.Visit(ast)
