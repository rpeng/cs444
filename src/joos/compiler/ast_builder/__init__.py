from expr import *
from stmt import *
from decl import *
from base import *


def BuildAST(parse_tree):
    builder = ASTBuilder()
    return builder.VisitParseTreeNode(parse_tree)
