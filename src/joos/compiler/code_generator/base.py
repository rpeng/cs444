from joos.compiler.code_generator.decl import DeclCodeMixin
from joos.compiler.code_generator.expr import ExprCodeMixin
from joos.compiler.code_generator.stmt import StmtCodeMixin
from joos.compiler.code_generator.tools.symbols import Symbols
from joos.compiler.code_generator.tools.namer import Namer
from joos.compiler.code_generator.tools.writer import Writer
from joos.syntax import ASTVisitor


class CodeGenerator(DeclCodeMixin, ExprCodeMixin, StmtCodeMixin, ASTVisitor):

    def __init__(self, compilation_unit, type_map, output_dir):
        self.compilation_unit = compilation_unit
        self.type_map = type_map
        self.output_dir = output_dir
        self.namer = Namer()
        self.filename = "{}/{}.s".format(output_dir,
                                         self.namer.Visit(self.compilation_unit))
        self.writer = Writer(self.filename)
        self.symbols = Symbols(self.writer)

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
        if node.value.token_type == 'INT':
            self.writer.OutputLine("mov eax, {}".format(node.value.lexeme))
        elif node.value.token_type == 'true':
            self.writer.OutputLine("mov eax, 1")
        elif node.value.token_type == 'false':
            self.writer.OutputLine("mov eax, 0")
        elif node.value.token_type == 'CHAR':
            self.writer.OutputLine("mov eax, {}".format(node.value.lexeme))
        elif node.value.token_type == 'null':
            self.writer.OutputLine("mov eax, 0")
        else: # STRING
            self.DefaultBehaviour(node)
