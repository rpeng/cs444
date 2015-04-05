from joos.compiler.code_generator.decl import DeclCodeMixin
from joos.compiler.code_generator.expr import ExprCodeMixin
from joos.compiler.code_generator.stmt import StmtCodeMixin
from joos.compiler.code_generator.tools.namer import Namer
from joos.compiler.code_generator.tools.writer import Writer
from joos.syntax import ASTVisitor


class CodeGenerator(DeclCodeMixin, ExprCodeMixin, StmtCodeMixin, ASTVisitor):

    def __init__(self, compilation_unit, type_map, output_dir):
        self.compilation_unit = compilation_unit
        self.type_map = type_map
        self.output_dir = output_dir
        self.namer = Namer()
        self.writer = Writer(self.namer, output_dir, self.compilation_unit)

    def Start(self):
        self.Visit(self.compilation_unit)

    # Base
    def Visit(self, node_or_list):
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    node.visit(self)
            else:
                return node_or_list.visit(self)

    def DefaultBehaviour(self, node):
        raise NotImplementedError

    def VisitCompilationUnit(self, node):
        self.Visit(node.type_decl)

    def VisitArrayType(self, node):
        self.DefaultBehaviour(node)

    def VisitClassOrInterfaceType(self, node):
        self.DefaultBehaviour(node)

    def VisitVoidType(self, node):
        self.DefaultBehaviour(node)

    def VisitPrimitiveType(self, node):
        self.DefaultBehaviour(node)

    def VisitName(self, node):
        self.DefaultBehaviour(node)

    def VisitLiteral(self, node):
        self.DefaultBehaviour(node)
