from compiler.parser import ParseTreeNode
from joos.syntax.abstract import rules_map


class BuilderVisitor(object):

    def VisitParseTreeNode(self, node):
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
        modifiers = self.VisitParseTreeNode(node.children[0]).modifiers
        name = node.children[2].token.lexeme
        body = self.VisitParseTreeNode(node.children[3])
        return klass(modifiers, name, body)

    def CreateModifiers(self, klass, node):
        modifiers = []
        if node.rule.rhs == ['Modifier']:
            modifiers.append(node[0][0].token)
        else:
            other_mods = self.VisitParseTreeNode(node[0])
            modifiers.extend(other_mods.modifiers)
            modifiers.append(node[1][0].token)
        return klass(modifiers)
