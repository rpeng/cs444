class DeclBuilderMixin(object):
    def CreateCompilationUnit(self, klass, node):
        (pkg_decl, import_decls, type_decls) = self._resolve(node,
                'PackageDeclaration', '+ImportDeclarations', '+TypeDeclarations')
        return klass(pkg_decl, import_decls, type_decls)

    def CreatePackageDecl(self, klass, node):
        (name,) = self._resolve(node, 'Name')
        name = name.name
        return klass(name)

    def CreateImportDecl(self, klass, node):
        (name,) = self._resolve(node[0], 'Name')
        name = name.name
        return klass(name)

    def CreateTypeDecl(self, klass, node):
        return self.VisitParseTreeNode(node[0])

    def CreateClassDecl(self, klass, node):
        (modifiers, name, extends, interfaces, body) = self._resolve(
            node, '+Modifiers', 'ID', 'Super', 'Interfaces', 'ClassBody')
        modifiers = [x[0].token for x in modifiers]
        name = name.token
        extends = extends[1][0][0].name

        (interfaces,) = self._resolve(interfaces, '+InterfaceTypeList')
        interfaces = [x[0][0].name for x in interfaces]

        (body,) = self._resolve(body, '+ClassBodyDeclarations')
        field_decls = []
        method_decls = []
        constructor_decls = []
        for class_body in body:
            if class_body.rule.rhs == ['ClassMemberDeclaration']:
                decl = class_body[0]
                if decl.rule.rhs == ['FieldDeclaration']:
                    field_decls.append(decl[0])
                else: # MethodDeclaration
                    method_decls.append(decl[0])
            else: # ConstructorDeclaration
                constructor_decls.append(class_body[0])
        return klass(modifiers, name, extends, interfaces, field_decls,
                method_decls, constructor_decls)

    def CreateMethodDecl(self, klass, node):
        (header, body) = self._resolve(node, 'MethodHeader', 'MethodBody')
        return klass(header, body)

    def CreateMethodHeader(self, klass, node):
        (modifiers, m_type, decl) = self._resolve(node, '+Modifiers', 
                'Type', 'MethodDeclarator')
        (m_id, m_param) = self._resolve(decl, 'ID', '+FormalParameterList')
        modifiers = [x[0].token for x in modifiers]
        if not m_type:
            m_type = node[1].token
        m_id = m_id.token
        return klass(modifiers, m_type, m_id, m_param)

    def CreateInterfaceDecl(self, klass, node):
        (name, extends_interface, body) = self._resolve(node, 'ID', 
                '+ExtendsInterfaces', 'InterfaceBody')
        name = name.token
        extends_interface = [x[0][0].name for x in extends_interface]
        (method_headers,) = self._resolve(body, '+InterfaceMemberDeclarations')
        if method_headers:
            method_headers = [x[0] for x in body]
        return klass(name, extends_interface, method_headers)

    def CreateFieldDecl(self, klass, node):
        (modifiers, f_type, var_decl) = self._resolve(node, '+Modifiers', 
                'Type', 'VariableDeclarator')
        modifiers = [x[0].token for x in modifiers]
        f_type = f_type.t_type
        return klass(modifiers, f_type, var_decl)

    def CreateConstructorDecl(self, klass, node):
        (modifiers, con_decl, body) = self._resolve(node, '+Modifiers', 
                'ConstructorDeclarator', 'ConstructorBody')
        modifiers = [x[0].token for x in modifiers]
        (name, params) = self._resolve(con_decl, 'SimpleName',
                '+FormalParameterList')
        name = name[0].token
        (body,) = self._resolve(body, '+BlockStatements')
        return klass(modifiers, name, params, body)

    def CreateVariableDecl(self, klass, node):
        (var_id, exp) = self._resolve(node, 'VariableDeclaratorId',
                'VariableInitializer')
        var_id = var_id[0].token
        if exp:
            exp = exp[0]
        return klass(var_id, exp)

    def CreateParameter(self, klass, node):
        (p_type, var_id) = self._resolve(node, 'Type', 'VariableDeclaratorId')
        p_type = p_type.t_type
        var_id = var_id[0].token
        return klass(p_type, var_id)

    def CreateName(self, klass, node):
        if node.rule.lhs == 'Name':
            return self.CreateName(klass, node[0])
        elif node.rule.lhs == 'SimpleName':
            return klass([node[0].token])
        else:
            lhs = self.CreateName(klass, node[0])
            return klass(lhs.name + [node[-1].token])
    
    def CreateType(self, klass, node):
        if node.rule.rhs[0] == 'PrimitiveType':
            (p_type,) = self._resolve(node, 'PrimitiveType')
            return klass(p_type.t_type)
        else:
            return klass(self.VisitParseTreeNode(node[0]))

    def CreatePrimitiveType(self, klass, node):
        if node.rule.rhs == ['boolean']:
            return klass(node[0].token)
        else:
            return klass(node[0][0].token)

    def CreateMethodInvocation(self, klass, node):
        if node.rule.rhs[0] == 'Name':
            (name, args) = self._resolve(node, 'Name', '+ArgumentList')
            name = name.name
        else:
            (primary, name, args) = self._resolve(node, 'Primary', 'ID', '+ArgumentList')
            name = name.token
        return klass(primary, name, args)

    def CreateBlock(self, klass, node):
        (block_stmts,) = self._resolve(node, '+BlockStatements')
        return klass(block_stmts)




