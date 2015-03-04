from joos.compiler.environment import Environment


class ExprEnvMixin(object):
    # Expression
    def VisitAssignmentExpression(self, node):
        self.PassVisit(node.env, node.lhs)
        self.PassVisit(node.env, node.exp)
        return Environment.Empty()

    def VisitBinaryExpression(self, node):
        self.PassVisit(node.env, node.left)
        self.PassVisit(node.env, node.right)
        return Environment.Empty()

    def VisitUnaryExpression(self, node):
        self.PassVisit(node.env, node.right)
        return Environment.Empty()

    def VisitCastExpression(self, node):
        self.PassVisit(node.env, node.cast_type)
        self.PassVisit(node.env, node.exp)
        return Environment.Empty()

    def VisitParensExpression(self, node):
        self.PassVisit(node.env, node.exp)
        return Environment.Empty()

    def VisitFieldAccess(self, node):
        self.PassVisit(node.env, node.primary)
        return Environment.Empty()

    def VisitArrayAccess(self, node):
        self.PassVisit(node.env, node.name_or_primary)
        return Environment.Empty()

    def VisitThisExpression(self, node):
        return Environment.Empty()

    def VisitArrayCreationExpression(self, node):
        self.PassVisit(node.env, node.a_type)
        self.PassVisit(node.env, node.exp)
        return Environment.Empty()

    def VisitStatementExpression(self, node):
        self.PassVisit(node.env, node.stmt)
        return Environment.Empty()

    def VisitNameExpression(self, node):
        self.PassVisit(node.env, node.name)
        return Environment.Empty()

    def VisitClassInstanceCreationExpression(self, node):
        self.PassVisit(node.env, node.class_type)
        self.PassVisit(node.env, node.args)
        return Environment.Empty()

    def VisitMethodInvocation(self, node):
        self.PassVisit(node.env, node.name)
        self.PassVisit(node.env, node.primary)
        self.PassVisit(node.env, node.args)
        return Environment.Empty()
