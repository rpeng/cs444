from joos.compiler.environment import Environment
from joos.errors import err
from joos.syntax import ASTVisitor, ImportDecl


class TypeLinker(ASTVisitor):
    def __init__(self, type_map):
        self.type_map = type_map

    def _LookupQualifiedType(self, name):
        split = name.Split()
        canon = name.AsString()

        for i in range(1, len(split)):
            prefix = '.'.join(split[:i])
            if self.type_map.LookupType(prefix) is not None:
                err(name.name[0],
                    "Prefix of qualified type should "
                    "not resolve to a type: " + canon +
                    ' prefix: ' + prefix)

        type = self.type_map.LookupType(canon)
        if type is None:
            err(name.name[0], "Type does not exist: " + canon)
        return type

    def DefaultBehaviour(self, node):
        return Environment.Empty()
        raise NotImplementedError

    def VisitParseTreeNode(self, node):
        return self.DefaultBehaviour(node)

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
        return self.DefaultBehaviour(node)

    def VisitArrayType(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassOrInterfaceType(self, node):
        return self.DefaultBehaviour(node)

    def VisitVoidType(self, node):
        return self.DefaultBehaviour(node)

    def VisitPrimitiveType(self, node):
        return self.DefaultBehaviour(node)

    def VisitName(self, node):
        return self.DefaultBehaviour(node)

    def VisitLiteral(self, node):
        return self.DefaultBehaviour(node)

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
            types = self.type_map.LookupPackage(canon)
            if types is None:
                err(node.name.tokens[0],
                    "Package does not exist: " + canon)
            env.AddPackageImport(canon, types)

        return env

    def VisitClassDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitInterfaceDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodHeader(self, node):
        return self.DefaultBehaviour(node)

    def VisitFieldDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitConstructorDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitVariableDeclarator(self, node):
        return self.DefaultBehaviour(node)

    def VisitLocalVarDecl(self, node):
        return self.DefaultBehaviour(node)

    def VisitParameter(self, node):
        return self.DefaultBehaviour(node)

    # Expression
    def VisitAssignmentExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitBinaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitUnaryExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitCastExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitParensExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitFieldAccess(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayAccess(self, node):
        return self.DefaultBehaviour(node)

    def VisitThisExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitArrayCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitStatementExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitNameExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitClassInstanceCreationExpression(self, node):
        return self.DefaultBehaviour(node)

    def VisitMethodInvocation(self, node):
        return self.DefaultBehaviour(node)

    # Statement
    def VisitBlock(self, node):
        return self.DefaultBehaviour(node)

    def VisitIfThenElseStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitWhileStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitForStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitReturnStatement(self, node):
        return self.DefaultBehaviour(node)

    def VisitEmptyStatement(self, node):
        return self.DefaultBehaviour(node)
