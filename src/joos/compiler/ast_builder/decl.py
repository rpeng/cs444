class DeclBuilderMixin(object):
    def CreatePackageDecl(self, klass, node):
        (name,) = self._resolve(node, 'Name')
        return klass(name.name)

    def CreateImportDecl(self, klass, node):
        (class_import, pkg_import) = self._resolve(
            node, 'ClassImportDeclaration', 'PackageImportDeclaration')
        (name,) = self._resolve(node[0], 'Name')
        if class_import:
            import_type = klass.CLASS_IMPORT
        else:
            import_type = klass.PACKAGE_IMPORT
        return klass(name.name, import_type)

    def CreateTypeDecl(self, klass, node):
        class_decl, interface_decl = self._resolve(
            node, 'ClassDeclaration', 'InterfaceDeclaration')
        return class_decl or interface_decl or None

    def CreateClassDecl(self, klass, node):
        (modifiers, name, extends, interfaces, body) = self._resolve(
            node, '+Modifiers', 'ID', 'Super', 'Interfaces', 'ClassBody')
        if modifiers:
            modifiers = [x[0].token for x in modifiers]  # Modifier
        name = name.token
        # ClassType, ClassOrInterfaceType, Name
        if extends:
            extends = extends[1][0].name

        if interfaces:
            (interfaces,) = self._resolve(interfaces, '+InterfaceTypeList')
            # ClassOrInterfaceType, Name
            interfaces = [x[0].name for x in interfaces]

        (body,) = self._resolve(body, '+ClassBodyDeclarations')
        field_decls = []
        method_decls = []
        constructor_decls = []
        if body:
            for class_body in body:
                if class_body.rule.rhs == ['ClassMemberDeclaration']:
                    decl = class_body[0]
                    if decl.rule.rhs == ['FieldDeclaration']:
                        field_decls.append(decl[0])
                    else:  # MethodDeclaration
                        method_decls.append(decl[0])
                else:  # ConstructorDeclaration
                    constructor_decls.append(class_body[0])
        return klass(modifiers, name, extends, interfaces, field_decls,
                     method_decls, constructor_decls)

    def CreateInterfaceDecl(self, klass, node):
        (name, extends_interface, body) = self._resolve(
            node, 'ID', '+ExtendsInterfaces', 'InterfaceBody')
        name = name.token
        # InterfaceType
        if extends_interface:
            extends_interface = [x[0].name for x in extends_interface]
        (method_headers,) = self._resolve(body, '+InterfaceMemberDeclarations')
        if method_headers:
            method_headers = [x[0] for x in method_headers]
        return klass(name, extends_interface, method_headers)

    def CreateMethodDecl(self, klass, node):
        (header, body) = self._resolve(node, 'MethodHeader', 'MethodBody')
        (block,) = self._resolve(body, 'Block')
        return klass(header, block)

    def CreateMethodHeader(self, klass, node):
        (modifiers, m_type, decl) = self._resolve(
            node, '+Modifiers', 'Type', 'MethodDeclarator')
        (m_id, params) = self._resolve(decl, 'ID', '+FormalParameterList')
        modifiers = [x[0].token for x in modifiers]
        if not m_type:
            m_type = self.VisitParseTreeNode(node[1])
        m_id = m_id.token
        return klass(modifiers, m_type, m_id, params)

    def CreateFieldDecl(self, klass, node):
        (modifiers, f_type, var_decl) = self._resolve(
            node, '+Modifiers', 'Type', 'VariableDeclarator')
        modifiers = [x[0].token for x in modifiers]
        return klass(modifiers, f_type, var_decl)

    def CreateConstructorDecl(self, klass, node):
        (modifiers, con_decl, body) = self._resolve(
            node, '+Modifiers', 'ConstructorDeclarator', 'ConstructorBody')
        modifiers = [x[0].token for x in modifiers]
        (name, params) = self._resolve(
            con_decl, 'SimpleName', '+FormalParameterList')
        name = name[0].token
        return klass(modifiers, name, params, body.Get('Block'))

    def CreateVariableDeclarator(self, klass, node):
        (var_id, exp) = self._resolve(
            node, 'VariableDeclaratorId', 'VariableInitializer')
        var_id = var_id[0].token
        if exp:
            exp = exp[0]
        return klass(var_id, exp)

    def CreateLocalVarDecl(self, klass, node):
        (l_type, var_decl) = self._resolve(node, 'Type', 'VariableDeclarator')
        return klass(l_type, var_decl)

    def CreateParameter(self, klass, node):
        (p_type, var_id) = self._resolve(node, 'Type', 'VariableDeclaratorId')
        var_id = var_id[0].token  # ID
        return klass(p_type, var_id)
