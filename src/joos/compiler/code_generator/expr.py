from joos.syntax import UnaryExpression


class ExprCodeMixin(object):
    # Expression
    def VisitAssignmentExpression(self, node):
        self.Visit(node.lhs)
        self.Visit(node.exp)

    def VisitBinaryExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitUnaryExpression(self, node):
        self.Visit(node.right)
        if node.sign.lexeme == UnaryExpression.MINUS:
            self.writer.OutputLine('neg eax')
        else:
            self.writer.OutputLine('sub eax, 1')
            self.writer.OutputLine('neg eax')

    def VisitCastExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitParensExpression(self, node):
        self.Visit(node.exp)

    def VisitFieldAccess(self, node):
        self.DefaultBehaviour(node)

    def VisitArrayAccess(self, node):
        self.DefaultBehaviour(node)

    def VisitThisExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitArrayCreationExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitStatementExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitNameExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitClassInstanceCreationExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        self.DefaultBehaviour(node)

