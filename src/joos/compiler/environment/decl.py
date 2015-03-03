from joos.compiler.environment import Environment


class DeclEnvMixin(object):
    def VisitPackageDecl(self, node):
        env = Environment()
        name = '.'.join([x.lexeme for x in node.name])
        env.AddPackage(name, node)
        return env

    def VisitImportDecl(self, node):
        return Environment.Empty()

    def VisitClassDecl(self, node):
        env = node.env.upstream.Fork()
        env.Update(self.ForkVisit(node.env, node.method_decls))
        env.Update(self.ForkVisit(node.env, node.constructor_decls))

        if node.field_decls:
            for decl in node.field_decls:
                update = self.PassVisit(env, decl)
                env = env.Fork()
                env.Update(update)
                node.env.Update(update)

        env = Environment()
        env.AddClassOrInterface(node.name.lexeme, node)
        return env

    def VisitInterfaceDecl(self, node):
        node.env.Update(self.ForkVisit(node.env, node.method_decls))

        env = Environment()
        env.AddClassOrInterface(node.name.lexeme, node)
        return env

    def VisitMethodDecl(self, node):
        node.env.Update(self.ForkVisit(node.env, node.header))
        node.env.Update(self.ForkVisit(node.env, node.body_block))

        env = Environment()
        env.AddMethod(node.header.m_id.lexeme, node)
        return env

    def VisitMethodHeader(self, node):
        env = Environment()
        env.Update(self.PassVisit(env, node.params))
        return env

    def VisitFieldDecl(self, node):
        node.env.Update(self.ForkVisit(node.env, node.var_decl))

        env = Environment()
        env.AddField(node.var_decl.var_id.lexeme, node)
        return env

    def VisitConstructorDecl(self, node):
        node.env.Update(self.PassVisit(node.env, node.params))
        self.ForkVisit(node.env, node.body)

        env = Environment()
        env.AddMethod(node.name.lexeme, node)
        return env

    def VisitVariableDeclarator(self, node):
        self.PassVisit(node.env, node.exp)
        return Environment.Empty()

    def VisitLocalVarDecl(self, node):
        self.ForkVisit(node.env, node.var_decl)

        env = Environment()
        env.AddLocalVar(node.var_decl.var_id.lexeme, node)
        return env

    def VisitParameter(self, node):
        env = Environment()
        env.AddParameter(node.var_id.lexeme, node)
        return env
