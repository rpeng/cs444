class EnvExprMixin(object):
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

    def VisitClassInstanceCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        return self.DefaultBehaviour(node)
