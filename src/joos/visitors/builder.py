from compiler.parser import ParseTreeNode
from joos.syntax.abstract import rules_map


class BuilderVisitor(object):

    def _resolve(self, rule, *accessors):
        result = []
        for accessor in accessors:
            child = rule.rule_map.get(accessor)
            if child:
                child = self.VisitParseTreeNode(child)
            result.append(child)
        return tuple(result)

    def VisitParseTreeNode(self, node):
        if not node:
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
        (modifiers, name, extends, interfaces, body) = self._resolve(node,
                'Modifiers', 'ID', 'Super', 'Interfaces', 'ClassBody')
        if modifiers:
            modifiers = modifiers.modifiers
        name = name.token
        return klass(modifiers, name, extends, interfaces, body)

    def CreateLiteral(self, klass, node):
        l_type = node[0].token
        value = ''
        if l_type.token_type == 'INT':
            value = int(node[0].token.lexeme)
        return klass(l_type, value)

    def CreateModifiers(self, klass, node):
        modifiers = []
        if node.rule.rhs == ['Modifier']:
            modifiers.append(node[0][0].token)
        else:
            other_mods = self.VisitParseTreeNode(node[0])
            modifiers.extend(other_mods.modifiers)
            modifiers.append(node[1][0].token)
        return klass(modifiers)

    def CreateInterfaceMethodDecl(self, klass, node):
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
        name = node[2].token
        extends_interface = ''
        body = self.VisitParseTreeNode(node[3])
        if node[3].rule.lhs != 'InterfaceBody':
            extends_interface = body
            body = self.VisitParseTreeNode(node[4])
        return klass(name, extends_interface, body)

    def CreateFieldDecl(self, klass, node):
        modifiers, decl_type, var_decl = self._resolve(node,
                'Modifiers', 'Type', 'VariableDeclarations')
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
        else: # MethodDeclaration
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
