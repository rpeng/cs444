from joos.compiler.environment import *
from joos.syntax import ASTVisitor


class EnvBuilder(DeclEnvMixin, ExprEnvMixin, StmtEnvMixin, ASTVisitor):
    # Base
    def ForkVisit(self, env, node_or_list):
        # Forks the env before passing it to the node
        # Use if node will mutate the environment
        updates = Environment()
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    updates.Update(self.ForkVisit(env, node))
            else:
                node_or_list.env = env.Fork()
                updates.Update(node_or_list.visit(self))
        return updates

    def PassVisit(self, env, node_or_list):
        # Passes the env by reference to the node
        # Use if node will NOT mutate the env
        updates = Environment()
        if node_or_list is not None:
            if isinstance(node_or_list, list):
                for node in node_or_list:
                    updates.Update(self.PassVisit(env, node))
            else:
                node_or_list.env = env
                updates.Update(node_or_list.visit(self))
        return updates

    def Visit(self, node):  # Entry point
        return node.visit(self)

    def DefaultBehaviour(self, node):
        raise NotImplementedError
        return Environment.Empty()

    def VisitCompilationUnit(self, node):
        env = Environment()

        env.Update(self.PassVisit(env, node.pkg_decl))
        env.Update(self.PassVisit(env, node.import_decls))
        env.Update(self.ForkVisit(env, node.type_decl))

        node.env = env
        return Environment.Empty()

    def VisitArrayType(self, node):
        self.PassVisit(node.env, node.type_or_name)
        return Environment.Empty()

    def VisitClassOrInterfaceType(self, node):
        return Environment.Empty()

    def VisitVoidType(self, node):
        return Environment.Empty()

    def VisitPrimitiveType(self, node):
        return Environment.Empty()

    def VisitName(self, node):
        return Environment.Empty()

    def VisitLiteral(self, node):
        return Environment.Empty()
