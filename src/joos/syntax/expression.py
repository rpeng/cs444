from joos.syntax.abstract import AbstractSyntaxNode

class Expression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateExpression(cls, node)

class Assignment(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateAssignment(cls, node)

    def visit(self, visitor):
        visitor.VisitAssignment(self)

    def __init__(self, lhs, exp):
        self.lhs = lhs
        self.exp = exp

class ConditionalOrExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateConditionalOrExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitConditionalOrExpression(self)

    def __init__(self, left, right):
        self.left = left
        self.right = right

class ConditionalAndExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateConditionalAndExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitConditionalAndExpression(self)

    def __init__(self, left, right):
        self.left = left
        self.right = right

class InclusiveOrExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateInclusiveOrExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitInclusiveOrExpression(self)

    def __init__(self, left, right):
        self.left = left
        self.right = right

class AndExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateAndExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitAndExpression(self)

    def __init__(self, left, right):
        self.left = left
        self.right = right

class EqualityExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateEqualityExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitEqualityExpression(self)

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class RelationalExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateRelationalExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitRelationalExpression(self)

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class AdditiveExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateAdditiveExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitAdditiveExpression(self)

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class MultiplicativeExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMultiplicativeExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitMultiplicativeExpression(self)

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateUnaryExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitUnaryExpression(self)

    def __init__(self, sign, right):
        self.sign = sign
        self.right = right

class UnaryExpressionNotPlusMinus(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateUnaryExpressionNotPlusMinus(cls, node)

    def visit(self, visitor):
        visitor.VisitUnaryExpressionNotPlusMinus(self)

    def __init__(self, sign, right):
        self.sign = sign
        self.right = right

class CastExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateCastExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitCastExpression(self)

    def __init__(self, cast_type, exp):
        self.cast_type = cast_type
        self.exp = exp

class FieldAccess(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldAccess(cls, node)

    def visit(self, visitor):
        visitor.VisitFieldAccess(self)

    def __init__(self, primary, name):
        self.primary = primary
        self.name = name

class ArrayAccess(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayAccess(cls, node)

    def visit(self, visitor):
        visitor.VisitArrayAccess(self)

    def __init__(self, name, exp):
        self.name = name
        self.exp = exp

class Primary(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePrimary(cls, node)

class PrimaryNoNewArray(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePrimaryNoNewArray(cls, node)

class ReferenceType(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateReferenceType(cls, node)

class ArrayType(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayType(cls, node)

class ArrayCreationExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayCreationExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitArrayCreationExpression(self)

    def __init__(self, p_type, exp):
        self.p_type = p_type
        self.exp = exp

class Literal(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateLiteral(cls, node)

    def visit(self, visitor):
        visitor.VisitLiteral(self)

    def __init__(self, token):
        self.token = token

class StatementExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateStatementExpression(cls, node)

class ClassInstanceCreationExpression(AbstractSyntaxNode):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassInstanceCreationExpression(cls, node)

    def visit(self, visitor):
        visitor.VisitClassInstanceCreationExpression(self)

    def __init__(self, class_type, args):
        self.class_type = class_type
        self.args = args
