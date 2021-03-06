class ExprBuilderMixin(object):
    def CreateExpression(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateAssignmentExpression(self, klass, node):
        if node.rule.lhs == 'AssignmentExpression':
            if node.rule.rhs[0] == 'ConditionalOrExpression':
                return self.VisitParseTreeNode(node[0])
            node = node[0]
        (lhs, exp) = self._resolve(
            node, 'LeftHandSide', 'AssignmentExpression')
        lhs = lhs[0]  # FieldAccess ArrayAccess
        result = klass(lhs, exp)
        result.debug_token = node[1].token
        return result

    def CreateBinaryExpression(self, klass, node):
        if node.rule.lhs != node.rule.rhs[0]:
            return self.VisitParseTreeNode(node[0])
        left = self.VisitParseTreeNode(node[0])
        op = node[1].token
        right = self.VisitParseTreeNode(node[2])
        return klass(left, op, right)

    def CreateUnaryExpression(self, klass, node):
        sign = node.Get('!')
        if sign is None:
            sign = node.Get('-')
        if sign is not None:
            expr = self.VisitParseTreeNode(node[1])
            return klass(sign.token, expr)
        else:
            return self.VisitParseTreeNode(node[0])

    def CreateCastExpression(self, klass, node):
        cast_type = self.VisitParseTreeNode(node[1])
        is_array = node.Get('Dims') is not None
        exp = self.VisitParseTreeNode(node[-1])
        return klass(cast_type, is_array, exp)

    def CreateFieldAccess(self, klass, node):
        (primary, name) = self._resolve(node, 'Primary', 'ID')
        name = name.token
        return klass(primary, name)

    def CreateArrayAccess(self, klass, node):
        if node.rule.rhs[0] == 'Name':
            (name, exp) = self._resolve(node, 'Name', 'Expression')
            return klass(name, exp)
        else:
            (name, exp) = self._resolve(
                node, 'PrimaryNoNewArray', 'Expression')
            return klass(name, exp)

    def CreatePrimary(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateParensExpression(self, klass, node):
        if node.rule.rhs[0] == '(':
            return klass(self.VisitParseTreeNode(node[1]))
        else:
            return self.VisitParseTreeNode(node[0])

    def CreateThisExpression(self, klass, node):
        return klass()

    def CreateArrayCreationExpression(self, klass, node):
        (a_type, exp) = self._resolve(node, 'PrimitiveType', 'DimExpr')
        if a_type is None:
            (a_type,) = self._resolve(node, 'ClassOrInterfaceType')
        exp = exp[1]
        return klass(a_type, exp)

    def CreateStatementExpression(self, klass, node):
        return klass(self.VisitParseTreeNode(node[0]))

    def CreateNameExpression(self, klass, node):
        return klass(self.VisitParseTreeNode(node[0]))

    def CreateClassInstanceCreationExpression(self, klass, node):
        (class_type, args) = self._resolve(node, 'ClassType', '+ArgumentList')
        class_type = class_type[0].name
        return klass(class_type, args)

    def CreateMethodInvocation(self, klass, node):
        (name, primary, primary_id, args) = self._resolve(
            node, 'Name', 'Primary', 'ID', '+ArgumentList')
        if primary_id is not None:
            primary_id = primary_id.token
        return klass(name, primary, primary_id, args)
