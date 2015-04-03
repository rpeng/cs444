from joos.syntax import ASTVisitor, UnaryExpression


class Evaluator(ASTVisitor):
    UNKNOWN = object()

    def __init__(self):
        pass

    def DefaultBehaviour(self, node):
        return Evaluator.UNKNOWN

    def VisitLiteral(self, node):
        token_type = node.value.token_type
        if token_type == 'INT' or token_type == '2147483648':
            return int(node.value.lexeme)
        elif token_type == 'CHAR':
            return str(node.value.lexeme)
        elif token_type == 'STRING':
            return str(node.value.lexeme)
        elif token_type == 'true':
            return True
        elif token_type == 'false':
            return False
        elif token_type == 'null':
            return Evaluator.UNKNOWN

    def VisitParensExpression(self, node):
        return self.Visit(node.exp)

    def VisitUnaryExpression(self, node):
        expr = self.Visit(node.right)
        if expr == Evaluator.UNKNOWN:
            return Evaluator.UNKNOWN

        if node.sign.lexeme == UnaryExpression.NEGATE:
            return not expr
        elif node.sign.lexeme == UnaryExpression.MINUS:
            return -expr
        return Evaluator.UNKNOWN

    def VisitBinaryExpression(self, node):
        left = self.Visit(node.left)
        right = self.Visit(node.right)
        op = node.op.lexeme
        if left == Evaluator.UNKNOWN or right == Evaluator.UNKNOWN:
            return Evaluator.UNKNOWN

        if op == '||' or op == '|':
            return left or right
        elif op == '&&' or op == '&':
            return left and right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            if right > 0:
                return left / right
        elif op == '%':
            return left % right

        return Evaluator.UNKNOWN
