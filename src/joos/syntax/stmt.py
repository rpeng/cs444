from joos.syntax import AbstractSyntaxNode


class Statement(AbstractSyntaxNode):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateStatement(cls, node)


class Block(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateBlock(cls, node)

    def visit(self, visitor):
        return visitor.VisitBlock(self)

    def __init__(self, stmts):
        self.stmts = stmts  # Statement[]


class IfThenElseStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateIfThenElseStatement(cls, node)

    def visit(self, visitor):
        return visitor.VisitIfThenElseStatement(self)

    def __init__(self, test_expr, stmt_true, stmt_false):
        self.test_expr = test_expr  # Expression
        self.stmt_true = stmt_true  # Statement
        self.stmt_false = stmt_false  # Statement


class WhileStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateWhileStatement(cls, node)

    def visit(self, visitor):
        return visitor.VisitWhileStatement(self)

    def __init__(self, test_expr, body):
        self.test_expr = test_expr  # Expression
        self.body = body  # Statement


class ForStatement(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateForStatement(cls, node)

    def visit(self, visitor):
        return visitor.VisitForStatement(self)

    def __init__(self, init, test_expr, update, body):
        self.init = init  # Expression | LocalVariableDecl
        self.test_expr = test_expr  # Expression
        self.update = update  # Expression
        self.body = body  # Statement


class LocalVarDeclStatement(AbstractSyntaxNode):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLocalVarDeclStatement(cls, node)
