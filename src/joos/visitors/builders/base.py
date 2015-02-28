from compiler.parser import ParseTreeNode
from joos.syntax import rules_map
from joos.visitors.builders import ExprBuilderMixin, DeclBuilderMixin, StmtBuilderMixin

class BuilderVisitor(ExprBuilderMixin, DeclBuilderMixin, StmtBuilderMixin):
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
        if node is None or not isinstance(node, ParseTreeNode):
            return node
        if node.rule and node.rule.lhs in rules_map:
            klass = rules_map[node.rule.lhs]
            new_node = klass.create(self, node)

            new_node.rule = node.rule
            new_node.token = node.token
            new_node.children = node.children
            return new_node
        else:
            children = []
            if node.children:
                for child in node.children:
                    children.append(self.VisitParseTreeNode(child))
            new_node = ParseTreeNode(node.token, node.rule, children)
            return new_node
