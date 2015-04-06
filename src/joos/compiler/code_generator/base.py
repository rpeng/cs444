import ast
from joos.compiler.code_generator import Vars
from joos.compiler.code_generator.decl import DeclCodeMixin
from joos.compiler.code_generator.expr import ExprCodeMixin
from joos.compiler.code_generator.stmt import StmtCodeMixin
from joos.compiler.code_generator.tools.symbols import Symbols
from joos.compiler.code_generator.tools.namer import Namer
from joos.compiler.code_generator.tools.writer import Writer
from joos.compiler.name_linker.disambiguator import NameType
from joos.compiler.type_checker import TypeChecker
from joos.syntax import ASTVisitor, Parameter, LocalVarDecl, FieldDecl


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
        self.types = TypeChecker(compilation_unit, type_map)
        self.vars = None

    def Start(self):
        self.Visit(self.compilation_unit)

    # Name loading logic
    def IterateLoadName(self, node):
        names = node.Split()

        # Eventually loads value to eax, location to ebx
        self.writer.OutputLine('; loading name {}'.format(names.AsString()))
        self.writer.OutputLine('mov eax, [ebp + 8]')  # move 'this' as starting point

        env = node.env
        kind = None
        for name in names:
            if kind == None:  # Check everything
                field = env.LookupField(name)
                if field:
                    offset = Vars.GetFieldOffset(field[1])
                    self.writer.OutputLine('; load subname {}'.format(name))
                    self.writer.OutputLine("mov eax, [eax]")
                    self.writer.OutputLine("add eax, {}".format(offset))
                    self.writer.OutputLine("lea ebx, [eax]")
                    self.writer.OutputLine("mov eax, [eax]")
            elif kind == NameType.EXPR:
                # Next must be a non-static field
                pass
            elif kind == NameType.PACKAGE:
                # Next one is either a package or a type
                pass
            elif kind == NameType.TYPE:
                # Next one has to be a static field
                pass

    # Base
    def Visit(self, node_or_list):
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    node.visit(self)
            else:
                return node_or_list.visit(self)

    def DefaultBehaviour(self, node):
        pass

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
        decl = node.context.linked
        if isinstance(decl, Parameter):
            offset = self.vars.GetParamOffset(decl)
            self.writer.OutputLine("mov eax, [ebp + {}]".format(offset))
            self.writer.OutputLine("lea ebx, [ebp + {}]".format(offset))
        elif isinstance(decl, LocalVarDecl):
            offset = self.vars.GetLocalVarOffset(decl)
            self.writer.OutputLine("mov eax, [ebp - {}]".format(offset))
            self.writer.OutputLine("lea ebx, [ebp - {}]".format(offset))
        elif isinstance(decl, FieldDecl):
            if decl.IsStatic():
                name = self.namer.Visit(decl)
                self.symbols.Import(name)
                self.writer.OutputLine("mov eax, [{}]".format(name))
                self.writer.OutputLine("lea ebx, [{}]".format(name))
            else:
                self.DefaultBehaviour(node)
        else:
            self.DefaultBehaviour(node)

    def VisitLiteral(self, node):
        if node.value.token_type == 'INT':
            self.writer.OutputLine("mov eax, {}".format(node.value.lexeme))
        elif node.value.token_type == 'true':
            self.writer.OutputLine("mov eax, 1")
        elif node.value.token_type == 'false':
            self.writer.OutputLine("mov eax, 0")
        elif node.value.token_type == 'CHAR':
            self.writer.OutputLine("mov eax, {}".format(
                ord(ast.literal_eval(node.value.lexeme))))
        elif node.value.token_type == 'null':
            self.writer.OutputLine("mov eax, 0")
        else: # STRING
            self.DefaultBehaviour(node)
