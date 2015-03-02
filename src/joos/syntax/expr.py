from joos.syntax import AbstractSyntaxNode


class Expression(AbstractSyntaxNode):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateExpression(cls, node)


class AssignmentExpression(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateAssignmentExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitAssignmentExpression(self)

    def __init__(self, lhs, exp):
        self.lhs = lhs  # Name | FieldAccess | ArrayAccess
        self.exp = exp  # Expression


class BinaryExpression(Expression):
    CONDITIONAL = ['||', '&&']
    INCLUSIVE = ['|', '&']
    EQUALITY = ['==', '!=']
    RELATIONAL = ['<', '>', '<=', '>=', 'instanceof']
    ARITHMETIC = ['+', '-', '*', '/', '%']

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateBinaryExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitBinaryExpression(self)

    def __init__(self, left, op, right):
        self.left = left  # Expression
        self.op = op  # token
        self.right = right  # Expression


class UnaryExpression(Expression):
    NEGATE = '!'
    MINUS = '-'

    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateUnaryExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitUnaryExpression(self)

    def __init__(self, sign, right):
        self.sign = sign  # token
        self.right = right  # Expression


class CastExpression(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateCastExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitCastExpression(self)

    def __init__(self, cast_type, is_array, exp):
        self.cast_type = cast_type  # PrimitiveType | Expression | Name
        self.is_array = is_array  # boolean
        self.exp = exp  # Expression


class ParensExpression(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateParensExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitParensExpression(self)

    def __init__(self, exp):
        self.exp = exp  # Expression


class FieldAccess(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateFieldAccess(cls, node)

    def visit(self, visitor):
        return visitor.VisitFieldAccess(self)

    def __init__(self, primary, name):
        self.primary = primary  # Primary
        self.name = name  # token


class ArrayAccess(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayAccess(cls, node)

    def visit(self, visitor):
        return visitor.VisitArrayAccess(self)

    def __init__(self, name_or_primary, exp):
        self.name_or_primary = name_or_primary  # Name | Primary
        self.exp = exp  # Expression


class Primary(Expression):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreatePrimary(cls, node)


class ThisExpression(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateThisExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitThisExpression(self)


class ArrayCreationExpression(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateArrayCreationExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitArrayCreationExpression(self)

    def __init__(self, a_type, exp):
        self.a_type = a_type  # PrimitiveType | ClassOrInterfaceType
        self.exp = exp  # Expression


class StatementExpression(Expression):
    # Abstract
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateStatementExpression(cls, node)


class ClassInstanceCreationExpression(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateClassInstanceCreationExpression(cls, node)

    def visit(self, visitor):
        return visitor.VisitClassInstanceCreationExpression(self)

    def __init__(self, class_type, args):
        self.class_type = class_type  # Name
        self.args = args  # Expression[]?


class MethodInvocation(Expression):
    @classmethod
    def create(cls, visitor, node):
        return visitor.CreateMethodInvocation(cls, node)

    def visit(self, visitor):
        return visitor.VisitMethodInvocation(self)

    def __init__(self, name, primary, primary_id, args):
        # Methods are either Name, or primary + id
        self.name = name  # Name?
        self.primary = primary  # Primary?
        self.primary_id = primary_id  # token?
        self.args = args  # Expression[]?
