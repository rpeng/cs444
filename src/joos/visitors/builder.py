from compiler.parser import ParseTreeNode
from joos.syntax.abstract import rules_map


class BuilderVisitor(object):

    def _resolve(self, node, *accessors):
        result = []
        for accessor in accessors:
            if (accessor.startswith('+')):  # expand
                child = node.rhs_map.get(accessor[1:])
                if child:
                    child = self._expand(child)
            else:
                child = node.rhs_map.get(accessor)
                if child:
                    child = self.VisitParseTreeNode(child)
            result.append(child)
        return tuple(result)

    def _expand(self, node):
        expanded = []
        if node:
            while True:
                if node.rule.rhs[0] == node.rule.lhs:
                    expanded.append(self.VisitParseTreeNode(node[-1]))
                    node = node[0]
                else:
                    expanded.append(self.VisitParseTreeNode(node[-1]))
                    break
        return expanded

    def VisitParseTreeNode(self, node):
        if node is None:
            return None
        if node.rule and node.rule.lhs in rules_map:
            klass = rules_map[node.rule.lhs]
            new_node = klass.create(self, node)

            new_node.rule = node.rule
            new_node.token = node.token
            new_node.children = node.children
            return new_node
        else:
            new_node = ParseTreeNode(node.token, node.rule)
            if node.children:
                for child in node.children:
                    new_node.children.append(self.VisitParseTreeNode(child))
            return new_node

    def CreateClassDecl(self, klass, node):
        (modifiers, name, extends, interfaces, body) = self._resolve(
            node, '+Modifiers', 'ID', 'Super', 'Interfaces', 'ClassBody')
        modifiers = [x[0].token for x in modifiers]
        name = name.token
        return klass(modifiers, name, extends, interfaces, body)

    def CreateLiteral(self, klass, node):
        l_type = node[0].token
        value = ''
        if l_type.token_type == 'INT':
            value = int(node[0].token.lexeme)
        return klass(l_type, value)

    def CreateInterfaceMemberDecl(self, klass, node):
        index = -1
        modifiers = []
        header = node[0]
        if header[0][0].rule.rhs[0] == 'Modifier':
            modifiers = self.VisitParseTreeNode(header[0]).modifiers
            index = 0
        m_type = self.VisitParseTreeNode(header[index+1])
        decl = self.VisitParseTreeNode(header[index+2])
        return klass(modifiers, m_type, decl)

    def CreateInterfaceDecl(self, klass, node):
        (name, extends_interface, body) = self._resolve(node, 'ID', 
                '+ExtendsInterfaces', 'InterfaceBody')
        name = name.token
        extends_interface = [x[0][0].name for x in extends_interface]
        return klass(name, extends_interface, body)

    def CreateName(self, klass, node):
        if node.rule.lhs == 'Name':
            return self.CreateName(klass, node[0])
        elif node.rule.lhs == 'SimpleName':
            return klass([node[0].token])
        else:
            lhs = self.CreateName(klass, node[0])
            return klass(lhs.name + [node[-1].token])

    def CreateFieldDecl(self, klass, node):
        modifiers, decl_type, var_decl = self._resolve(
            node, 'Modifiers', 'Type', 'VariableDeclarations')
        if modifiers:
            modifiers = modifiers.modifiers
        return klass(modifiers, decl_type, var_decl)

    def CreateClassMemberDecl(self, klass, node):
        modifiers = []
        cf_type = node.rule.rhs[0]
        decl = None
        body = None
        if cf_type == 'FieldDeclaration':
            modifiers = self.VisitParseTreeNode(node[0][0]).modifiers
            decl = self.VisitParseTreeNode(node[0][-1]).token
        else:  # MethodDeclaration
            modifiers = self.VisitParseTreeNode(node[0]).modifiers
            decl = self.VisitParseTreeNode(node[0][0][-1][0]).token
            body = self.VisitParseTreeNode(node[0][-1])
        return klass(modifiers, cf_type, decl, body)

    def CreateMethodDecl(self, klass, node):
        header = node[0]
        modifiers = self.VisitParseTreeNode(header[0]).modifiers
        m_type = self.VisitParseTreeNode(header[1])
        decl = self.VisitParseTreeNode(header[2])
        body = self.VisitParseTreeNode(node[1])
        if not body[0]:
            body = None
        return klass(modifiers, m_type, decl, body)
