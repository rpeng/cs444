class ExprCodeMixin(object):
    # Expression
    def VisitAssignmentExpression(self, node):
        raise NotImplementedError

    def VisitBinaryExpression(self, node):
        raise NotImplementedError

    def VisitUnaryExpression(self, node):
        raise NotImplementedError

    def VisitCastExpression(self, node):
        raise NotImplementedError

    def VisitParensExpression(self, node):
        raise NotImplementedError

    def VisitFieldAccess(self, node):
        raise NotImplementedError

    def VisitArrayAccess(self, node):
        raise NotImplementedError

    def VisitThisExpression(self, node):
        raise NotImplementedError

    def VisitArrayCreationExpression(self, node):
        raise NotImplementedError

    def VisitStatementExpression(self, node):
        raise NotImplementedError

    def VisitNameExpression(self, node):
        raise NotImplementedError

    def VisitClassInstanceCreationExpression(self, node):
        raise NotImplementedError

    def VisitMethodInvocation(self, node):
        raise NotImplementedError

