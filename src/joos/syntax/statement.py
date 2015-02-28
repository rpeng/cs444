from joos.syntax.abstract import AbstractSyntaxNode
from structs.cfg import Rule

class BlockStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateBlockStatement(cls, node)

class Statement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateStatement(cls, node)

class StatementWithoutTrailingSubstatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateStatementWithoutTrailingSubstatement(cls, node)

class IfThenStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateIfThenStatement(cls, node)

    def visit(self, visitor):
        visitor.VisitIfThenStatement(self)

    def __init__(self, exp, stmt):
        self.exp = exp
        self.stmt = stmt

class IfThenElseStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateIfThenElseStatement(cls, node)

    def visit(self, visitor):
        visitor.VisitIfThenElseStatement(self)

    def __init__(self, exp, stmt_true, stmt_false):
        self.exp = exp
        self.stmt_true = stmt_true
        self.stmt_false = stmt_false

class WhileStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateWhileStatement(cls, node)

    def visit(self, visitor):
        visitor.VisitWhileStatement(self)

    def __init__(self, exp, stmt):
        self.exp = exp
        self.stmt = stmt

class ForStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateForStatement(cls, node)

    def visit(self, visitor):
        visitor.VisitForStatement(self)

    def __init__(self, init, exp, update, stmt):
        self.init = init
        self.exp = exp
        self.update = update
        self.stmt = stmt

class LocalVarDecl(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLocalVarDecl(cls, node)

    def visit(self, visitor):
        visitor.VisitLocalVarDecl(self)

    def __init__(self, l_type, var_decl):
        self.l_type = l_type
        self.var_decl = var_decl

