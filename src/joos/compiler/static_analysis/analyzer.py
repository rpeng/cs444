from joos.compiler.static_analysis.evaluator import Evaluator
from joos.errors import err
from joos.syntax import ASTVisitor, VoidType


class StaticAnalyzer(ASTVisitor):
    def __init__(self, comp_unit, type_map):
        self.comp_unit = comp_unit
        self.type_map = type_map

        self.saw_return = None  # saw return statement
        self.evaluator = Evaluator()
        self.infinite_loop = False  # we're in an infinite loop

    def Start(self):
        self.Visit(self.comp_unit)

    def DefaultBehaviour(self, node):
        pass

    def ScopeEnd(self):
        self.saw_return = None

    def VisitCompilationUnit(self, node):
        self.Visit(node.type_decl)

    # Decls
    def VisitPackageDecl(self, node):
        pass

    def VisitImportDecl(self, node):
        pass

    def VisitClassDecl(self, node):
        self.Visit(node.method_decls)
        self.Visit(node.constructor_decls)

    def VisitMethodDecl(self, node):
        should_ret = not isinstance(node.header.m_type, VoidType)
        self.infinite_loop = False
        self.saw_return = False

        if node.body_block:
            self.Visit(node.body_block)
            if not self.infinite_loop:
                if should_ret and not self.saw_return:
                    err(node.header.m_id, "Expected return statement.")

    def VisitConstructorDecl(self, node):
        self.Visit(node.body)

    # Statement
    def VisitBlock(self, node):
        self.saw_return = False
        if node.stmts:
            for stmt in node.stmts:
                if self.saw_return or self.infinite_loop:
                    err(node[0].token, "Unreachable statement.")
                self.Visit(stmt)

    def VisitIfThenElseStatement(self, node):
        node1_ret = False
        node2_ret = False

        self.Visit(node.test_expr)
        self.Visit(node.stmt_true)
        node1_ret = self.saw_return
        self.saw_return = False

        self.Visit(node.stmt_false)
        node2_ret = self.saw_return
        self.saw_return = node1_ret and node2_ret
        self.infinite_loop = False

    def VisitWhileStatement(self, node):
        result = self.evaluator.Visit(node.test_expr)
        if result is False:
            err(node[0].token, "Unreachable statement in while loop.")
        if result is True:
            self.infinite_loop = True
        self.Visit(node.body)
        self.saw_return = False

    def VisitForStatement(self, node):
        result = True
        self.Visit(node.body)
        if node.test_expr is not None:
            result = self.evaluator.Visit(node.test_expr)
        if result is False:
            err(node[0].token, "Unreachable statement in for loop.")
        if result is True:
            self.infinite_loop = True
        self.saw_return = False

    def VisitReturnStatement(self, node):
        self.saw_return = True

    def VisitEmptyStatement(self, node):
        pass
