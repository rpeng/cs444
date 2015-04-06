from joos.compiler.type_checker.type_kind import TypeKind
from joos.syntax import UnaryExpression, BinaryExpression


class ExprCodeMixin(object):

    def InvokeMethod(self, method_name, args):
        if args is None:
            args = []
        for (i, arg) in enumerate(args):
            self.writer.OutputLine('; argument {}'.format(i))
            self.Visit(arg)
            self.writer.OutputLine('push eax')
        self.writer.OutputLine('call {}'.format(method_name))
        self.writer.OutputLine('add esp, {}'.format(len(args) * 4))

    # Expression
    def VisitAssignmentExpression(self, node):
        self.Visit(node.lhs)  # addr in ebx
        self.writer.OutputLine('push ebx')
        self.Visit(node.exp)
        self.writer.OutputLine('pop ebx')
        self.writer.OutputLine('mov [ebx], eax')

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
        elif node.op.lexeme == '==':
            equal = self.writer.NewLabel('equal')
            self.Visit(node.left)
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('cmp eax, ebx')
            self.writer.OutputLine('mov eax, 1')
            self.writer.OutputLine('je {}'.format(equal))
            self.writer.OutputLine('mov eax, 0')
            self.writer.OutputLabel(equal)
        elif node.op.lexeme == '!=':
            not_equal = self.writer.NewLabel('not_equal')
            self.Visit(node.left)
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('cmp eax, ebx')
            self.writer.OutputLine('mov eax, 0')
            self.writer.OutputLine('je {}'.format(not_equal))
            self.writer.OutputLine('mov eax, 1')
            self.writer.OutputLabel(not_equal)
        elif node.op.lexeme in BinaryExpression.RELATIONAL:
            relational = self.writer.NewLabel('relational')
            self.Visit(node.left)
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('cmp ebx, eax')
            self.writer.OutputLine('mov eax, 1')
            if node.op.lexeme == '>':
                self.writer.OutputLine('jg {}'.format(relational))
            elif node.op.lexeme == '<':
                self.writer.OutputLine('jl {}'.format(relational))
            elif node.op.lexeme == '>=':
                self.writer.OutputLine('jge {}'.format(relational))
            elif node.op.lexeme == '<=':
                self.writer.OutputLine('jle {}'.format(relational))
            self.writer.OutputLine('mov eax, 0')
            self.writer.OutputLabel(relational)
        elif node.op.lexeme == 'instanceof':
            self.DefaultBehaviour(node)
        elif node.op.lexeme == '+':
            left_kind = self.types.Visit(node.left)
            right_kind = self.types.Visit(node.right)
            if (left_kind.kind in TypeKind.numerics and right_kind.kind in TypeKind.numerics):
                self.Visit(node.left)
                self.writer.OutputLine('push eax')
                self.Visit(node.right)
                self.writer.OutputLine('pop ebx')
                self.writer.OutputLine('add eax, ebx')
            else: #STRING
                self.DefaultBehaviour(node)
        elif node.op.lexeme == '-':
            self.Visit(node.left)
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('sub ebx, eax')
            self.writer.OutputLine('mov eax, ebx')
        elif node.op.lexeme == '*':
            self.Visit(node.left)
            self.writer.OutputLine('push eax')
            self.Visit(node.right)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('push edx')
            self.writer.OutputLine('imul eax, ebx')
            self.writer.OutputLine('pop edx')
        elif node.op.lexeme == '/':
            self.writer.OutputLine('push edx')
            self.Visit(node.right)
            self.writer.OutputLine('push eax')
            self.Visit(node.left)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('cdq')
            self.writer.OutputLine('idiv ebx')
            self.writer.OutputLine('pop edx')
        elif node.op.lexeme == '%':
            self.writer.OutputLine('push edx')
            self.Visit(node.right)
            self.writer.OutputLine('push eax')
            self.Visit(node.left)
            self.writer.OutputLine('pop ebx')
            self.writer.OutputLine('cdq')
            self.writer.OutputLine('idiv ebx')
            self.writer.OutputLine('mov eax, edx')
            self.writer.OutputLine('pop edx')
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
        self.writer.OutputLine('mov eax, [ebp+8]')

    def VisitArrayCreationExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitStatementExpression(self, node):
        self.Visit(node.stmt)

    def VisitNameExpression(self, node):
        return self.Visit(node.name)

    def VisitClassInstanceCreationExpression(self, node):
        self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        method_name = self.namer.Visit(node.linked_method)
        if node.linked_method.IsStatic():
            self.writer.OutputLine('; Static method invocation')
            self.InvokeMethod(method_name, node.args)
        else:
            self.DefaultBehaviour(node)

