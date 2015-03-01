class ExprPrinterMixin(object):
    def VisitAssignmentExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitBinaryExpression(self, node):
        return """{i}BinaryExpression
{i}  Operator: {op}
{i}  Left:
{leftexpr}
{i}  Right:
{rightexpr}
""".format(i=self.i(), op=node.op.lexeme,
           leftexpr=self.n(node.left),
           rightexpr=self.n(node.right))

    def VisitUnaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitCastExpression(self, node):
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

    def VisitClassInstanceCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        return self.DefaultBehaviour(node)
