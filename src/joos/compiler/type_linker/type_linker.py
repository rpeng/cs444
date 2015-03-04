from joos.compiler.environment import Environment
from joos.compiler.type_linker.resolver import Resolver
from joos.errors import err
from joos.syntax import ASTVisitor, ImportDecl, Name


class TypeLinker(ASTVisitor):
    def __init__(self, type_map):
        self.type_map = type_map
        self.resolver = Resolver(self.type_map)

    def _LookupQualifiedType(self, name):
        split = name.Split()
        canon = name.AsString()

        for i in range(1, len(split)):
            prefix = '.'.join(split[:i])
            # Allow default package prefix
            if prefix not in self.type_map.decls:
                if self.type_map.LookupType(prefix) is not None:
                    err(name.tokens[0],
                        "Prefix of qualified type should "
                        "not resolve to a type: " + canon +
                        ' prefix: ' + prefix)

        type = self.type_map.LookupType(canon)
        if type is None:
            err(name.tokens[0], "Type does not exist: " + canon)
        return type

    def DefaultBehaviour(self, node):
        raise NotImplementedError

    def VisitParseTreeNode(self, node):
        return self.DefaultBehaviour(node)

    def Resolve(self, name_or_list):
        if name_or_list is None:
            return

        if isinstance(name_or_list, list):
            for name in name_or_list:
                self.resolver.Resolve(name)
        else:
            self.resolver.Resolve(name_or_list)

    # Base
    def Visit(self, node_or_list):
        env = Environment()
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    env.Update(node.visit(self))
            else:
                env.Update(node_or_list.visit(self))
        return env

    def VisitCompilationUnit(self, node):
        node.env.Update(self.Visit(node.import_decls))

        # Implicitly import java.lang.*
        types = self.type_map.LookupPackage('java.lang')
        if types is not None:
            node.env.AddPackageImport('java.lang', types)

        self.Visit(node.type_decl)
        return Environment.Empty()

    def VisitArrayType(self, node):
        if isinstance(node.type_or_name, Name):
            self.Resolve(node.type_or_name)
        else:
            self.Visit(node.type_or_name)
        return Environment.Empty()

    def VisitClassOrInterfaceType(self, node):
        self.Resolve(node.name)
        return Environment.Empty()

    def VisitVoidType(self, node):
        return Environment.Empty()

    def VisitPrimitiveType(self, node):
        return Environment.Empty()

    def VisitName(self, node):
        return Environment.Empty()

    def VisitLiteral(self, node):
        return Environment.Empty()

    # Decl
    def VisitPackageDecl(self, node):
        return Environment.Empty()

    def VisitImportDecl(self, node):
        env = Environment()

        if node.import_type == ImportDecl.CLASS_IMPORT:
            type = self._LookupQualifiedType(node.name)
            node.name.linked_type = type
            env.AddClassImport(node.name, type)
        else:  # Package Import
            canon = node.name.AsString()
            own_pkg = node.env.LookupPackage()
            if not (own_pkg and canon == own_pkg[0]):
                types = self.type_map.LookupPackage(canon)
                if types is None:
                    err(node.name.tokens[0],
                        "Package does not exist: " + canon)
                env.AddPackageImport(canon, types)
        return env

    def VisitClassDecl(self, node):
        self.Resolve(node.extends)
        self.Resolve(node.interfaces)
        self.Visit(node.field_decls)
        self.Visit(node.method_decls)
        self.Visit(node.constructor_decls)
        return Environment.Empty()

    def VisitInterfaceDecl(self, node):
        self.Resolve(node.extends_interface)
        self.Visit(node.method_decls)
        return Environment.Empty()

    def VisitMethodDecl(self, node):
        self.Visit(node.header)
        self.Visit(node.body_block)
        return Environment.Empty()

    def VisitMethodHeader(self, node):
        self.Visit(node.m_type)
        self.Visit(node.params)
        return Environment.Empty()

    def VisitFieldDecl(self, node):
        self.Visit(node.f_type)
        self.Visit(node.var_decl)
        return Environment.Empty()

    def VisitConstructorDecl(self, node):
        self.Visit(node.params)
        self.Visit(node.body)
        return Environment.Empty()

    def VisitVariableDeclarator(self, node):
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitLocalVarDecl(self, node):
        self.Visit(node.l_type)
        self.Visit(node.var_decl)
        return Environment.Empty()

    def VisitParameter(self, node):
        self.Visit(node.p_type)
        return Environment.Empty()

    # Expression
    def VisitAssignmentExpression(self, node):
        self.Visit(node.lhs)
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitBinaryExpression(self, node):
        self.Visit(node.left)
        self.Visit(node.right)
        return Environment.Empty()

    def VisitUnaryExpression(self, node):
        self.Visit(node.right)
        return Environment.Empty()

    def VisitCastExpression(self, node):
        if isinstance(node.cast_type, Name):
            self.Resolve(node.cast_type)
        else:
            self.Visit(node.cast_type)
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitParensExpression(self, node):
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitFieldAccess(self, node):
        self.Visit(node.primary)
        return Environment.Empty()

    def VisitArrayAccess(self, node):
        if not isinstance(node.name_or_primary, Name):
            self.Visit(node.name_or_primary)
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitThisExpression(self, node):
        return Environment.Empty()

    def VisitArrayCreationExpression(self, node):
        self.Visit(node.a_type)
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitStatementExpression(self, node):
        self.Visit(node.stmt)
        return Environment.Empty()

    def VisitNameExpression(self, node):
        return Environment.Empty()

    def VisitClassInstanceCreationExpression(self, node):
        self.Resolve(node.class_type)
        self.Visit(node.args)
        return Environment.Empty()

    def VisitMethodInvocation(self, node):
        self.Visit(node.primary)
        self.Visit(node.args)
        return Environment.Empty()

    # Statement
    def VisitBlock(self, node):
        self.Visit(node.stmts)
        return Environment.Empty()

    def VisitIfThenElseStatement(self, node):
        self.Visit(node.test_expr)
        self.Visit(node.stmt_true)
        self.Visit(node.stmt_false)
        return Environment.Empty()

    def VisitWhileStatement(self, node):
        self.Visit(node.test_expr)
        self.Visit(node.body)
        return Environment.Empty()

    def VisitForStatement(self, node):
        self.Visit(node.init)
        self.Visit(node.test_expr)
        self.Visit(node.update)
        self.Visit(node.body)
        return Environment.Empty()

    def VisitReturnStatement(self, node):
        self.Visit(node.exp)
        return Environment.Empty()

    def VisitEmptyStatement(self, node):
        return Environment.Empty()
