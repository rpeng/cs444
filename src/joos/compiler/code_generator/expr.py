class ExprCodeMixin(object):
    # Expression
    def VisitAssignmentExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitBinaryExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitUnaryExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitCastExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitParensExpression(self, node):
        self.DefaultBehaviour(node)

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

