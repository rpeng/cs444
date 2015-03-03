from joos.compiler.environment import Environment


class StmtEnvMixin(object):
    # Statement
    def VisitBlock(self, node):
        env = node.env.upstream.Fork()
        if node.stmts:
            for stmt in node.stmts:
                update = self.ForkVisit(env, stmt)
                env = env.Fork()
                env.Update(update)

        return Environment.Empty()

    def VisitIfThenElseStatement(self, node):
        self.PassVisit(node.env, node.test_expr)
        self.ForkVisit(node.env, node.stmt_true)
        self.ForkVisit(node.env, node.stmt_false)
        return Environment.Empty()

    def VisitWhileStatement(self, node):
        self.PassVisit(node.env, node.test_expr)
        self.ForkVisit(node.env, node.body)
        return Environment.Empty()

    def VisitForStatement(self, node):
        node.env.Update(self.PassVisit(node.env, node.init))
        self.PassVisit(node.env, node.test_expr)
        self.PassVisit(node.env, node.update)
        self.ForkVisit(node.env, node.body)
        return Environment.Empty()

    def VisitReturnStatement(self, node):
        self.PassVisit(node.env, node.exp)
        return Environment.Empty()

    def VisitEmptyStatement(self, node):
        return Environment.Empty()
