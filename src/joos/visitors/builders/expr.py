class ExprBuilderMixin(object):
    def CreateExpression(self, klass, node):
        if node[0].rule.rhs == ['ConditionalOrExpression']:
            return self.VisitParseTreeNode(node[0][0])
        return self.VisitParseTreeNode(node[0])

    def CreateAssignment(self, klass, node):
        (lhs, exp) = self._resolve(
            node, 'LeftHandSide', 'AssignmentExpression')
        if lhs.rule.rhs == ['Name']:
            lhs = lhs[0].name
        else:
            lhs = lhs[0]  # FieldAccess ArrayAccess
        return klass(lhs, exp)

    def CreateConditionalOrExpression(self, klass, node):
        if node.rule.rhs[0] == 'ConditionalAndExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'ConditionalOrExpression', 'ConditionalAndExpression')
            return klass(left, right)

    def CreateConditionalAndExpression(self, klass, node):
        if node.rule.rhs[0] == 'InclusiveOrExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'ConditionalAndExpression', 'InclusiveOrExpression')
            return klass(left, right)

    def CreateInclusiveOrExpression(self, klass, node):
        if node.rule.rhs[0] == 'AndExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'InclusiveOrExpression', 'AndExpression')
            return klass(left, right)

    def CreateAndExpression(self, klass, node):
        if node.rule.rhs[0] == 'EqualityExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'AndExpression', 'EqualityExpression')
            return klass(left, right)

    def CreateEqualityExpression(self, klass, node):
        if node.rule.rhs[0] == 'RelationalExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'EqualityExpression', 'RelationalExpression')
            operator = node[1].token
            return klass(left, operator, right)

    def CreateRelationalExpression(self, klass, node):
        if node.rule.rhs[0] == 'AdditiveExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            if node.rule.rhs[1] == 'instanceof':
                (left, right) = self._resolve(
                    node, 'RelationalExpression', 'ReferenceType')
            else:
                (left, right) = self._resolve(
                    node, 'RelationalExpression', 'AdditiveExpression')
            operator = node[1].token
            return klass(left, operator, right)

    def CreateAdditiveExpression(self, klass, node):
        if node.rule.rhs[0] == 'MultiplicativeExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'AdditiveExpression', 'MultiplicativeExpression')
            operator = node[1].token
            return klass(left, operator, right)

    def CreateMultiplicativeExpression(self, klass, node):
        if node.rule.rhs[0] == 'UnaryExpression':
            return self.VisitParseTreeNode(node[0])
        else:
            (left, right) = self._resolve(
                node, 'MultiplicativeExpression', 'UnaryExpression')
            operator = node[1].token
            return klass(left, operator, right)

    def CreateUnaryExpression(self, klass, node):
        if node.rule.rhs[0] == 'UnaryExpressionOrMaxInt':
            (sign, right) = self._resolve(node, '-', 'UnaryExpressionOrMaxInt')
            return klass(sign, right[0])
        else:
            return self.VisitParseTreeNode(node[0])

    def CreateUnaryExpressionNotPlusMinus(self, klass, node):
        if node.rule.rhs[0] == '!':
            (sign, right) = self._resolve(node, '!', 'UnaryExpression')
            return klass(sign, right)
        elif node.rule.rhs[0] == 'PostfixExpression':
            return self.VisitParseTreeNode(node[0][0])
        else:
            return self.VisitParseTreeNode(node[0])

    def CreateCastExpression(self, klass, node):
        if node.rule.rhs[-1] == 'UnaryExpression':
            (p_type, exp) = self._resolve(
                node, 'PrimitiveType', 'UnaryExpression')
            return klass(p_type, exp)
        elif node.rule.rhs[1] == 'Expression':
            (name, exp) = self._resolve(
                node, 'Expression', 'UnaryExpressionNotPlusMinus')
            return klass(name, exp)
        else:
            (name, exp) = self._resolve(
                node, 'Name', 'UnaryExpressionNotPlusMinus')
            return klass(name, exp)

    def CreateArrayAccess(self, klass, node):
        if node.rule.rhs[0] == 'Name':
            (name, exp) = self._resolve(node, 'Name', 'Expression')
            return klass(name, exp)
        else:
            (name, exp) = self._resolve(
                node, 'PrimaryNoNewArray', 'Expression')
            return klass(name, exp)

    def CreatePrimaryNoNewArray(self, klass, node):
        if node.rule.rhs[0] == '(':
            return self.VisitParseTreeNode(node[1])
        else:
            return self.VisitParseTreeNode(node[0])

    def CreateReferenceType(self, klass, node):
        if node.rule.rhs[0] == 'ClassOrInterfaceType':
            (ci,) = self._resolve(node, 'ClassOrInterfaceType')
            return ci[0]
        else:
            return self.VisitParseTreeNode(node[0])

    def CreateArrayType(self, klass, node):
        return node[0]

    def CreateFieldAccess(self, klass, node):
        (primary, name) = self._resolve(node, 'Primary', 'ID')
        name = name.token
        return klass(primary, name)

    def CreatePrimary(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateLiteral(self, klass, node):
        if node.rule.lhs == '2147483648':
            return klass(node.token)
        else:
            return klass(node[0].token)

    def CreateArrayCreationExpression(self, klass, node):
        (p_type, exp) = self._resolve(node[0], 'PrimitiveType', 'DimExpr')
        exp = exp[1]
        return klass(p_type, exp)

    def CreateStatementExpression(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateClassInstanceCreationExpression(self, klass, node):
        (class_type, args) = self._resolve(node, 'ClassType', '+ArgumentList')
        class_type = class_type[0][0].name
        return klass(class_type, args)
