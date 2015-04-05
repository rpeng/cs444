from joos.syntax import UnaryExpression


class ExprCodeMixin(object):
    # Expression
    def VisitAssignmentExpression(self, node):
        self.Visit(node.lhs)
        self.Visit(node.exp)

    def VisitBinaryExpression(self, node):
        if node.op.lexeme == '|':
            self.Visit(node.left)  # lhs in eax
            self.writer.OutputLine('push eax')
            self.Visit(node.right)  # rhs in eax
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('or eax, ebx')
        elif node.op.lexeme == '&':
            self.Visit(node.left)  # lhs in eax
            self.writer.OutputLine('push eax')
            self.Visit(node.right)  # rhs in eax
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('and eax, ebx')
        elif node.op.lexeme == '||':
            or_end = self.writer.NewLabel('or_end')
            self.Visit(node.left)
            self.writer.OutputLine('mov ebx, 0')
            self.writer.OutputLine('cmp eax, 1')
            self.writer.OutputLine('je {}'.format(or_end))
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLabel(or_end)
            self.writer.OutputLine('or eax, ebx')
        elif node.op.lexeme == '&&':
            and_end = self.writer.NewLabel('and_end')
            self.Visit(node.left)
            self.writer.OutputLine('mov ebx, 0')
            self.writer.OutputLine('cmp eax, 0')
            self.writer.OutputLine('je {}'.format(and_end))
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLabel(and_end)
            self.writer.OutputLine('and eax, ebx')
        else:
            self.DefaultBehaviour(node)

    def VisitUnaryExpression(self, node):
        self.Visit(node.right)
        if node.sign.lexeme == UnaryExpression.MINUS:
            self.writer.OutputLine('neg eax')
        else:
            self.writer.OutputLine('sub eax, 1')
            self.writer.OutputLine('neg eax')

    def VisitCastExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitParensExpression(self, node):
        self.Visit(node.exp)

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

