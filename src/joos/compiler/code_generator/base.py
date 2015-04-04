from joos.compiler.code_generator.decl import DeclCodeMixin
from joos.compiler.code_generator.expr import ExprCodeMixin
from joos.compiler.code_generator.stmt import StmtCodeMixin
from joos.syntax import ASTVisitor


class CodeGenerator(DeclCodeMixin, ExprCodeMixin, StmtCodeMixin, ASTVisitor):

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
        raise NotImplementedError

    def VisitArrayType(self, node):
        raise NotImplementedError

    def VisitClassOrInterfaceType(self, node):
        raise NotImplementedError

    def VisitVoidType(self, node):
        raise NotImplementedError

    def VisitPrimitiveType(self, node):
        raise NotImplementedError

    def VisitName(self, node):
        raise NotImplementedError

    def VisitLiteral(self, node):
        raise NotImplementedError
