from joos.compiler.hierarchy_check.common import GetStringDecl, StrSig
from joos.compiler.name_linker.disambiguator import NameType
from joos.compiler.type_checker.access_check import AccessChecker
from joos.compiler.type_checker.assignable import *
from joos.syntax import *


class TypeChecker(ASTVisitor):
    def DefaultBehaviour(self, node):
        raise NotImplementedError

    def __init__(self, comp, type_map):
        self.comp = comp
        self.type_map = type_map
        self.ret_type = None
        self.is_static = None
        self.class_decl = None
        self.initializer = None
        self.access_checker = AccessChecker(type_map)

        self.string_type = TypeKind(TypeKind.REF, GetStringDecl())

    def ArgsSig(self, args):
        sig = []
        if args:
            for arg in args:
                kind = self.Visit(arg)
                sig.append(kind.AsSig())
        return tuple(sig)

    def MethodSig(self, node):
        sig = []
        if node.name:
            sig.append(node.name.Last())
        else:
            sig.append(node.primary_id.lexeme)
        sig.extend(self.ArgsSig(node.args))
        return tuple(sig)

    def Start(self):
        self.comp.visit(self)

    def CheckNameInitializer(self, node):
        if node.Split()[0] == self.initializer:
            err(node.tokens[0], "Name in own initializer")

    # Base
    def Visit(self, node_or_list):
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    node.visit(self)
            else:
                return node_or_list.visit(self)

    def VisitCompilationUnit(self, node):
        self.Visit(node.type_decl)
        return None

    def VisitArrayType(self, node):
        if isinstance(node.type_or_name, Type):
            context = self.Visit(node.type_or_name)
            return TypeKind(TypeKind.ARRAY, context)
        elif isinstance(node.type_or_name, Name):
            return TypeKind(TypeKind.ARRAY,
                            TypeKind(TypeKind.REF, node.type_or_name.linked_type))

    def VisitClassOrInterfaceType(self, node):
        return TypeKind(TypeKind.REF, node.name.linked_type)

    def VisitVoidType(self, node):
        return TypeKind(TypeKind.VOID)

    def VisitPrimitiveType(self, node):
        token_type = node.t_type.token_type
        if token_type == 'boolean':
            return TypeKind(TypeKind.BOOL)
        elif token_type == 'byte':
            return TypeKind(TypeKind.BYTE)
        elif token_type == 'char':
            return TypeKind(TypeKind.CHAR)
        elif token_type == 'int':
            return TypeKind(TypeKind.INT)
        elif token_type == 'short':
            return TypeKind(TypeKind.SHORT)
        elif token_type == 'void':
            return TypeKind(TypeKind.VOID)

    def VisitName(self, node):
        self.CheckNameInitializer(node)
        self.access_checker.CheckName(node, is_static=self.is_static)

        if node.linked_type is ArrayType.LengthDecl:
            return TypeKind(TypeKind.INT, decl=ArrayType.LengthDecl)
        elif node.name_type == NameType.TYPE:
            return TypeKind(TypeKind.CLASS, node.linked_type)
        elif isinstance(node.linked_type, TypeDecl):
            return TypeKind(TypeKind.REF, node.linked_type)
        else:
            return self.Visit(node.linked_type)

    def VisitLiteral(self, node):
        token_type = node.value.token_type
        if token_type == 'INT' or token_type == '2147483648':
            return TypeKind.FromIntegral(node.value.lexeme)
        elif token_type == 'CHAR':
            return TypeKind(TypeKind.CHAR)
        elif token_type == 'STRING':
            return self.string_type
        elif token_type == 'true' or token_type == 'false':
            return TypeKind(TypeKind.BOOL)
        elif token_type == 'null':
            return TypeKind(TypeKind.NULL)

    # Decl
    def VisitPackageDecl(self, node):
        return None

    def VisitImportDecl(self, node):
        return None

    def VisitClassDecl(self, node):
        self.class_decl = node
        self.Visit(node.field_decls)
        self.Visit(node.method_decls)
        self.Visit(node.constructor_decls)
        if node.extends is not None:
            # Check for zero-arg constructor of extends
            zero_arg_cons = node.extends.linked_type.cons_map.get(())
            if not zero_arg_cons:
                err(node.name, "Superclass missing zero argument constructor")
        self.class_decl = None
        return TypeKind(TypeKind.REF, node)

    def VisitInterfaceDecl(self, node):
        return TypeKind(TypeKind.REF, node)

    def VisitMethodDecl(self, node):
        self.ret_type = self.Visit(node.header.m_type)
        result = self.ret_type

        self.is_static = node.IsStatic()
        self.Visit(node.body_block)
        self.ret_type = None
        self.is_static = None
        return result

    def VisitFieldDecl(self, node):
        lhs = self.Visit(node.f_type)

        self.is_static = node.IsStatic()
        rhs = self.Visit(node.var_decl)
        if rhs is not None:
            CheckAssignable(node.modifiers[0], lhs, rhs)

        self.is_static = None
        lhs.decl = node
        return lhs

    def VisitConstructorDecl(self, node):
        self.Visit(node.body)
        decl = node.env.LookupClassOrInterface()
        return TypeKind(TypeKind.REF, decl[1])

    def VisitVariableDeclarator(self, node):
        return self.Visit(node.exp)

    def VisitLocalVarDecl(self, node):
        lhs = self.Visit(node.l_type)

        self.initializer = node.var_decl.var_id.lexeme
        rhs = self.Visit(node.var_decl)
        self.initializer = None

        CheckAssignable(node.var_decl.var_id, lhs, rhs)
        lhs.decl = node
        return lhs

    def VisitParameter(self, node):
        return self.Visit(node.p_type)

    # Expression
    def VisitAssignmentExpression(self, node):
        lhs = self.Visit(node.lhs)
        exp = self.Visit(node.exp)
        CheckAssignable(node.debug_token, lhs, exp)
        if lhs.decl is ArrayType.LengthDecl:
            err(node.debug_token, "Cannot assign to array length")
        return lhs

    def VisitBinaryExpression(self, node):
        op = node.op.lexeme
        left = self.Visit(node.left)
        right = self.Visit(node.right)
        if op in BinaryExpression.CONDITIONAL or op in BinaryExpression.INCLUSIVE:
            CheckCastable(node[1].token, TypeKind.BOOL, left)
            CheckCastable(node[1].token, TypeKind.BOOL, right)
            return TypeKind(TypeKind.BOOL)
        elif op in BinaryExpression.RELATIONAL:
            CheckCastable(node[1].token, TypeKind.INT, left)
            CheckCastable(node[1].token, TypeKind.INT, right)
            return TypeKind(TypeKind.BOOL)
        elif op in BinaryExpression.ARITHMETIC:
            if op == '+':
                # For implicit String concatenations
                if (left.kind == TypeKind.VOID or right.kind == TypeKind.VOID):
                    err(node[1].token, "Invalid operands to + operator")
                if (CanCompare(TypeKind.INT, left)
                    and CanCompare(TypeKind.INT, right)):
                    return TypeKind(TypeKind.INT)
                elif (CanCompare(self.string_type, left) or
                      CanCompare(self.string_type, right)):
                    return self.string_type
                else:
                    err(node[1].token, "Invalid operands to + operator")
            else:
                CheckCastable(node[1].token, TypeKind.INT, left)
                CheckCastable(node[1].token, TypeKind.INT, right)
                return TypeKind(TypeKind.INT)
        elif op == BinaryExpression.INSTANCEOF:
            CheckComparable(node[1].token, left, right)
            return TypeKind(TypeKind.BOOL)
        if op in BinaryExpression.EQUALITY:
            if ((left.kind in TypeKind.numerics and right.kind in TypeKind.numerics)
                or (left.kind == TypeKind.BOOL and right.kind == TypeKind.BOOL)):
                return TypeKind(TypeKind.BOOL)
            if left.kind in TypeKind.references and right.kind in TypeKind.references:
                CheckComparable(node[1].token, left, right)
                return TypeKind(TypeKind.BOOL)
            else:
                err(node[1].token, "Cannot compare {} and {}".format(left, right))

    def VisitUnaryExpression(self, node):
        sign = node.sign.lexeme
        if sign == UnaryExpression.NEGATE:
            right = self.Visit(node.right)
            CheckCastable(node[0].token, TypeKind.BOOL, right)
            return TypeKind(TypeKind.BOOL)
        elif sign == UnaryExpression.MINUS:
            right = self.Visit(node.right)
            CheckCastable(node[0].token, TypeKind.INT, right)
            return TypeKind(TypeKind.INT)

    def VisitCastExpression(self, node):
        cast_type = self.Visit(node.cast_type)
        if node.is_array:
            cast_type = TypeKind(TypeKind.ARRAY, cast_type)
        exp = self.Visit(node.exp)

        if (exp.kind == TypeKind.CLASS):
            err(node[0].token, "Unexpected cast of a class")
        CheckCastable(node[0].token, cast_type, exp)

        if cast_type.kind == TypeKind.CLASS:
            cast_type.kind = TypeKind.REF
        return cast_type

    def VisitParensExpression(self, node):
        result = self.Visit(node.exp)
        if result.kind == TypeKind.CLASS:
            err(node[0].token, "Class in parens expression")
        return result

    def VisitFieldAccess(self, node):
        prim = self.Visit(node.primary)
        if prim.kind == TypeKind.REF:
            name = node.name.lexeme
            decl = prim.context.env.LookupField(name)
            if not decl:
                err(node.name, "Type {} has no field {}".format(prim, name))
            node.linked_type = decl
            return self.Visit(decl.f_type)
        elif prim.kind == TypeKind.ARRAY:
            if node.name.lexeme == "length":
                return TypeKind(TypeKind.INT)
            else:
                err(node.name, "Invalid field access on array "+node.name.lexeme)
        else:
            err(node.name, "Invalid field access")

    def VisitArrayAccess(self, node):
        lhs = self.Visit(node.name_or_primary)
        if lhs.kind != TypeKind.ARRAY:
            err(node[1].token, "Primary must be an array")
        exp = self.Visit(node.exp)
        CheckCanConvert(node[1].token, TypeKind.INT, exp)
        return lhs.context

    def VisitThisExpression(self, node):
        if self.is_static:
            err(node.token, "Cannot use 'this' in static context")
        decl = node.env.LookupClassOrInterface()
        return TypeKind(TypeKind.REF, decl[1])

    def VisitArrayCreationExpression(self, node):
        array_kind = self.Visit(node.a_type)
        exp_kind = self.Visit(node.exp)
        CheckCanConvert(node[0].token, TypeKind.INT, exp_kind)
        return TypeKind(TypeKind.ARRAY, array_kind)

    def VisitStatementExpression(self, node):
        return self.Visit(node.stmt)

    def VisitNameExpression(self, node):
        return self.Visit(node.name)

    def VisitClassInstanceCreationExpression(self, node):
        sig = self.ArgsSig(node.args)
        decl = node.class_type.linked_type
        if isinstance(decl, InterfaceDecl) or decl.IsAbstract():
            err(node[0].token, "Attempt to instantiate abstract class or interface")
        linked = decl.cons_map.get(sig)
        if linked:
            node.linked_type = linked
        else:
            err(node[0].token, "Constructor not found matching sig: {}"
                .format(StrSig(sig)))

        self.access_checker.CheckConstructor(node)

        return TypeKind(TypeKind.REF, decl)

    def VisitMethodInvocation(self, node):

        if node.name:  # Name method
            self.CheckNameInitializer(node.name)

            sig = self.MethodSig(node)
            if node.linked_decl == ArrayType.LengthDecl:
                err(node[1].token, "Cannot invoke array length")
            linked = node.linked_decl.method_map.get(sig)
            if not linked:
                err(node[1].token, "Method not found matching sig: {}"
                    .format(StrSig(sig)))
            node.linked_method = linked
            self.access_checker.CheckMethodName(node, self.is_static)
        else:  # Primary + ID
            # TODO: access check
            type_kind = self.Visit(node.primary)
            if type_kind.kind not in TypeKind.references:
                err(node[1].token, "{} cannot be dereferenced"
                    .format(type_kind.kind))
            sig = self.MethodSig(node)
            linked = type_kind.context.method_map.get(sig)
            if not linked:
                err(node[1].token, "Method not found matching sig: {}"
                    .format(StrSig(sig)))
            node.linked_method = linked
            node.linked_decl = type_kind.context
        return self.Visit(linked.header.m_type)

    # Statement
    def VisitBlock(self, node):
        self.Visit(node.stmts)
        return None

    def VisitIfThenElseStatement(self, node):
        test_type = self.Visit(node.test_expr)
        if test_type.kind != TypeKind.BOOL:
            err(node[0].token, "Expected boolean in if test")
        self.Visit(node.stmt_true)
        self.Visit(node.stmt_false)
        return None

    def VisitWhileStatement(self, node):
        test_type = self.Visit(node.test_expr)
        if test_type.kind != TypeKind.BOOL:
            err(node[0].token, "Expected boolean in while test")
        self.Visit(node.body)
        return None

    def VisitForStatement(self, node):
        test_type = self.Visit(node.test_expr)
        if test_type.kind != TypeKind.BOOL:
            err(node[0].token, "Expected boolean in for test")
        self.Visit(node.init)
        self.Visit(node.update)
        self.Visit(node.body)
        return None

    def VisitReturnStatement(self, node):
        if self.ret_type is None or self.ret_type == TypeKind(TypeKind.VOID):
            if node.exp is None:
                return None
            else:
                err(node[0].token, "Expression in void return")

        ret = self.Visit(node.exp)
        if ret is None:
            ret = TypeKind(TypeKind.VOID)

        CheckCanConvert(node[0].token, self.ret_type, ret)
        return None

    def VisitEmptyStatement(self, node):
        return None
