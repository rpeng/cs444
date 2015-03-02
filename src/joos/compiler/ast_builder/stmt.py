class StmtBuilderMixin(object):
    def CreateStatement(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateBlock(self, klass, node):
        (block_stmts,) = self._resolve(node, '+BlockStatements')
        if block_stmts is not None:
            block_stmts = [x[0] for x in block_stmts]
        return klass(block_stmts)

    def CreateIfThenElseStatement(self, klass, node):
        (test_expr,) = self._resolve(node, 'Expression')
        stmt_true = self.VisitParseTreeNode(node[4])
        if (node.rule.lhs == 'IfThenElseStatement' or
                node.rule.lhs == 'IfThenElseStatementNoShortIf'):
            stmt_false = self.VisitParseTreeNode(node[-1])
        else:
            stmt_false = None
        return klass(test_expr, stmt_true, stmt_false)

    def CreateWhileStatement(self, klass, node):
        (test_expr, body, body_no_if) = self._resolve(
            node, 'Expression', 'Statement', 'StatementNoShortIf')
        body = body or body_no_if
        return klass(test_expr, body)

    def CreateForStatement(self, klass, node):
        (init, exp, update, stmt, stmt_no_if) = self._resolve(
            node, 'ForInit', 'Expression', 'ForUpdate',
            'Statement', 'StatementNoShortIf')
        stmt = stmt or stmt_no_if
        return klass(init and init[0], exp, update and update[0], stmt)

    def CreateLocalVarDeclStatement(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateReturnStatement(self, klass, node):
        return klass(node.Get('Expression'))

    def CreateEmptyStatement(self, klass, node):
        return klass()
