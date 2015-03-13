from joos.compiler.type_checker.assignable import *
from joos.syntax import ASTVisitor


class TypeChecker(ASTVisitor):

    def DefaultBehaviour(self, node):
        raise NotImplementedError

    def __init__(self, comp, type_map):
        self.comp = comp
        self.type_map = type_map
        self.ret_type = None

    def Start(self):
        self.comp.visit(self)

    # Base
    def Visit(self, node_or_list):
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    node.visit(self)
            else:
                return node_or_list.visit(self)

    def VisitCompilationUnit(self, node):
        self.Visit(node.type_decl)
        return None

    def VisitArrayType(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassOrInterfaceType(self, node):
        return self.DefaultBehaviour(node)

    def VisitVoidType(self, node):
        return TypeKind(TypeKind.VOID)

    def VisitPrimitiveType(self, node):
        token_type = node.t_type.token_type
        if token_type == 'boolean':
            return TypeKind(TypeKind.BOOL)
        elif token_type == 'byte':
            return TypeKind(TypeKind.BYTE)
        elif token_type == 'char':
            return TypeKind(TypeKind.CHAR)
        elif token_type == 'int':
            return TypeKind(TypeKind.INT)
        elif token_type == 'short':
            return TypeKind(TypeKind.SHORT)
        elif token_type == 'void':
            return TypeKind(TypeKind.VOID)

    def VisitName(self, node):
        return self.DefaultBehaviour(node)

    def VisitLiteral(self, node):
        token_type = node.value.token_type
        if token_type == 'INT' or token_type == '2147483648':
            return TypeKind.FromIntegral(node.value.lexeme)
        elif token_type == 'CHAR':
            return TypeKind(TypeKind.CHAR)
        elif token_type == 'STRING':
            return TypeKind(TypeKind.STRING)
        elif token_type == 'true' or token_type == 'false':
            return TypeKind(TypeKind.BOOL)
        elif token_type == 'null':
            return TypeKind(TypeKind.NULL)

    # Decl
    def VisitPackageDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitImportDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassDecl(self, node):
        self.Visit(node.field_decls)
        self.Visit(node.method_decls)
        self.Visit(node.constructor_decls)
        return None

    def VisitInterfaceDecl(self, node):
        return None

    def VisitMethodDecl(self, node):
        self.ret_type = self.Visit(node.header.m_type)
        self.Visit(node.body_block)
        self.ret_type = None
        return None

    def VisitFieldDecl(self, node):
        lhs = self.Visit(node.f_type)
        rhs = self.Visit(node.var_decl)
        CheckAssignable(node.modifiers[0], lhs, rhs)
        return None

    def VisitConstructorDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitVariableDeclarator(self, node):
        return self.Visit(node.exp)

    def VisitLocalVarDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        return self.DefaultBehaviour(node)

    # Expression
    def VisitAssignmentExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitBinaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitUnaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitCastExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitParensExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitFieldAccess(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayAccess(self, node):
        return self.DefaultBehaviour(node)

    def VisitThisExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitStatementExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitNameExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassInstanceCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        return self.DefaultBehaviour(node)

    # Statement
    def VisitBlock(self, node):
        self.Visit(node.stmts)
        return None

    def VisitIfThenElseStatement(self, node):
        test_type = self.Visit(node.test_expr)
        if test_type.kind != TypeKind.BOOL:
            err(node[0].token, "Expected boolean in if statement")
        self.Visit(node.stmt_true)
        self.Visit(node.stmt_false)
        return None

    def VisitWhileStatement(self, node):
        test_type = self.Visit(node.test_expr)
        if test_type.kind != TypeKind.BOOL:
            err(node[0].token, "Expected boolean in if statement")
        self.Visit(node.body)
        return None

    def VisitForStatement(self, node):
        test_type = self.Visit(node.test_expr)
        if test_type.kind != TypeKind.BOOL:
            err(node[0].token, "Expected boolean in if statement")
        self.Visit(node.init)
        self.Visit(node.update)
        self.Visit(node.body)
        return None

    def VisitReturnStatement(self, node):
        ret = self.Visit(node.exp)
        if ret is None:
            ret = TypeKind(TypeKind.VOID)
        CheckAssignable(node[0].token, self.ret_type, ret)
        return None

    def VisitEmptyStatement(self, node):
        return None

