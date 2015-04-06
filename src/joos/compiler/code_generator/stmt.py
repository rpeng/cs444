from joos.compiler.environment import Environment


class StmtCodeMixin(object):
    # Statement
    def VisitBlock(self, node):
        self.vars = self.vars.NewBlock()
        self.Visit(node.stmts)
        self.vars = self.vars.EndBlock()

    def VisitIfThenElseStatement(self, node):
        statement_false = self.writer.NewLabel('statement_false')
        statement_end = self.writer.NewLabel('statement_end')
        self.Visit(node.test_expr)
        self.writer.OutputLine('cmp eax, 0')
        self.writer.OutputLine('je {}'.format(statement_false))
        # statement true
        self.Visit(node.stmt_true)
        self.writer.OutputLine('jmp {}'.format(statement_end))
        self.writer.OutputLabel(statement_false)
        # statement false
        self.Visit(node.stmt_false)
        self.writer.OutputLabel(statement_end)

    def VisitWhileStatement(self, node):
        statement_begin = self.writer.NewLabel('statement_begin')
        statement_end = self.writer.NewLabel('statement_end')
        self.writer.OutputLabel(statement_begin)
        self.Visit(node.test_expr)
        self.writer.OutputLine('cmp eax, 0')
        self.writer.OutputLine('je {}'.format(statement_end))
        self.Visit(node.body)
        self.writer.OutputLine('jmp {}'.format(statement_begin))
        self.writer.OutputLabel(statement_end)

    def VisitForStatement(self, node):
        statement_begin = self.writer.NewLabel('statement_begin')
        statement_end = self.writer.NewLabel('statement_end')
        self.Visit(node.init)
        self.writer.OutputLabel(statement_begin)
        self.Visit(node.test_expr)
        self.writer.OutputLine('cmp eax, 0')
        self.writer.OutputLine('je {}'.format(statement_end))
        self.Visit(node.body)
        self.Visit(node.update)
        self.writer.OutputLine('jmp {}'.format(statement_begin))
        self.writer.OutputLabel(statement_end)

    def VisitReturnStatement(self, node):
        if node.exp:
            self.Visit(node.exp)
        self.writer.OutputLine('leave')
        self.writer.OutputLine('ret')

    def VisitEmptyStatement(self, node):
        pass
