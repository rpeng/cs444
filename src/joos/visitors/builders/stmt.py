class StmtBuilderMixin(object):
    def CreateBlockStatement(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateStatement(self, klass, node):
        return self.VisitParseTreeNode(node[0])
        
    def CreateStatementWithoutTrailingSubstatement(self, klass, node):
        if node.rule.rhs == ['EmptyStatement']:
            return self.VisitParseTreeNode(node[0][0])
        elif node.rule.rhs == ['ExpressionStatement']:
            return self.VisitParseTreeNode(node[0][0][0])
        elif node.rule.rhs == ['ReturnStatement']:
            return self.VisitParseTreeNode(node[0][1])
        return self.VisitParseTreeNode(node[0])
    
    def CreateIfThenStatement(self, klass, node):
        (exp, stmt) = self._resolve(node, 'Expression', 'Statement')
        return klass(exp, stmt)

    def CreateIfThenElseStatement(self, klass, node):
        if node.rule.lhs == 'IfThenElseStatement':
            (exp, stmt_no_short_if, stmt) = self._resolve(node, 
                'Expression', 'StatementNoShortIf', 'Statement')
        else:
            (exp, stmt_no_short_if, stmt) = self._resolve(node, 
                'Expression', 'StatementNoShortIf', 'StatementNoShortIf')
        return klass(exp, stmt_no_short_if, stmt)
    
    def CreateWhileStatement(self, klass, node):
        if node.rule.lhs == 'WhileStatement':
            (exp, stmt) = self._resolve(node, 'Expression', 'Statement')
        else:
            (exp, stmt) = self._resolve(node, 'Expression', 'StatementNoShortIf')
        return klass(exp, stmt)

    def CreateForStatement(self, klass, node):
        if node.rule.lhs == 'ForStatement':
            (init, exp, update, stmt) = self._resolve(node, 'ForInit',
                'Expression', 'ForUpdate', 'Statement')
        else:
            (init, exp, update, stmt) = self._resolve(node, 'ForInit',
                'Expression', 'ForUpdate', 'StatementNoShortIf')
        if init.rule.rhs[0] == 'StatementExpressionList':
            (init,) = self._resolve(init, '+StatementExpressionList')
        else:
            init = init[0]
        return klass(init, exp, update[0], stmt)
    
    def CreateLocalVarDecl(self, klass, node):
        if node.rule.lhs == 'LocalVariableDeclarationStatement':
            node = node[0]
        (l_type, var_decl) = self._resolve(node, 'Type', 'VariableDeclarator')
        l_type = l_type.t_type
        return klass(l_type, var_decl)
        
