from joos.compiler.type_checker.type_kind import TypeKind
from joos.syntax import UnaryExpression, BinaryExpression


class ExprCodeMixin(object):

    def PushArguments(self, args):
        for (i, arg) in enumerate(args):
            self.writer.OutputLine('; argument {}'.format(i))
            self.Visit(arg)
            self.writer.OutputLine('push eax')

    def InvokeStaticMethod(self, method_name, args):
        if args is None:
            args = []
        self.PushArguments(args)
        self.writer.OutputLine('call {}'.format(method_name))
        self.writer.OutputLine('add esp, {}'.format(len(args) * 4))

    def InvokeConstructorMethod(self, method_name, args):
        # Assumes 'this' pointer is in ecx
        if args is None:
            args = []
        self.PushArguments(args)
        self.writer.OutputLine('push ecx')  # this
        self.writer.OutputLine('call {}'.format(method_name))
        self.writer.OutputLine('add esp, {}'.format(len(args) * 4 + 4))

    def InvokeInstanceMethod(self, method_decl, args):
        # Assumes 'this' pointer is in ecx
        if args is None:
            args = []
        for (i, arg) in enumerate(args):
            self.writer.OutputLine('; argument {}'.format(i))
            self.Visit(arg)
            self.writer.OutputLine('push eax')

        self.writer.OutputLine('push ecx')
        # Before we call the method, we need to look it up in the vtable
        offset = self.vars.GetMethodOffset(method_decl)
        self.writer.OutputLine('mov eax, [ecx]')
        self.writer.OutputLine('add eax, {}'.format(offset))
        self.writer.OutputLine('call [eax]')
        self.writer.OutputLine('add esp, {}'.format(len(args) * 4 + 4))

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
        class_type = node.linked_type.env.LookupClassOrInterface()[1]
        class_name = self.namer.Visit(class_type)

        class_creator = "new~{}".format(class_name)
        class_cons = self.namer.Visit(node.linked_type)

        self.symbols.Import(class_creator)
        self.symbols.Import(class_cons)

        self.writer.OutputLine("; creating class {}".format(class_name))
        self.writer.OutputLine("call {}".format(class_creator))

        self.vars.Push() # for extra ecx on stack
        self.writer.OutputLine("push ecx")
        self.writer.OutputLine("mov ecx, eax")
        self.InvokeConstructorMethod(class_cons, node.args)
        self.writer.OutputLine("mov eax, ecx")
        self.writer.OutputLine("pop ecx")
        self.vars.Pop()


    def VisitMethodInvocation(self, node):
        method_name = self.namer.Visit(node.linked_method)
        # A.b.c()
        if node.linked_method.IsStatic():
            self.writer.OutputLine('; Static method invocation')
            self.symbols.Import(method_name)
            self.InvokeStaticMethod(method_name, node.args)
        else:
            self.writer.OutputLine('; Instance method locate this')

            # Need to get 'this' and put it in eax
            if node.name is not None: # A.b.c()
                self.finder.ResolveName(node.name, self.vars, skip_last=True)
            elif node.primary is not None: # (A.b()).c()
                self.Visit(node.primary)

            self.writer.OutputLine('; Instance method invocation')
            self.vars.Push()
            self.writer.OutputLine("push ecx")
            self.writer.OutputLine("mov ecx, eax")
            self.InvokeInstanceMethod(node.linked_method, node.args)
            self.writer.OutputLine("mov eax, ecx")
            self.writer.OutputLine("pop ecx")
            self.vars.Pop()
