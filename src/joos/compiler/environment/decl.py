from joos.compiler.environment import Environment


class DeclEnvMixin(object):
    def VisitPackageDecl(self, node):
        env = Environment()
        env.AddPackage(node.name.AsString(), node)
        return env

    def VisitImportDecl(self, node):
        return Environment.Empty()

    def VisitClassDecl(self, node):
        env = node.env.upstream.Fork()
        self.PassVisit(env, node.extends)
        self.PassVisit(env, node.interfaces)
        env.Update(self.ForkVisit(env, node.method_decls))
        env.Update(self.ForkVisit(env, node.constructor_decls))

        if node.field_decls:
            for decl in node.field_decls:
                update = self.PassVisit(env, decl)
                env = env.Fork()
                env.Update(update)

        node.env = env

        env = Environment()
        env.AddClassOrInterface(node.name.lexeme, node)
        return env

    def VisitInterfaceDecl(self, node):
        node.env.Update(self.ForkVisit(node.env, node.method_decls))
        self.PassVisit(node.env, node.extends_interface)

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
        self.PassVisit(node.env, node.m_type)
        self.PassVisit(node.env, node.params)

        env = Environment()
        env.Update(self.PassVisit(node.env, node.params))
        return env

    def VisitFieldDecl(self, node):
        node.env.Update(self.ForkVisit(node.env, node.var_decl))
        self.PassVisit(node.env, node.f_type)
        self.PassVisit(node.env, node.var_decl)

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
        self.PassVisit(node.env, node.l_type)

        env = Environment()
        env.AddLocalVar(node.var_decl.var_id.lexeme, node)
        return env

    def VisitParameter(self, node):
        self.PassVisit(node.env, node.p_type)

        env = Environment()
        env.AddParameter(node.var_id.lexeme, node)
        return env
