from lexer.parser import ParseTreeNode
from joos.syntax import rules_map
from joos.compiler.ast_builder import *


class ASTBuilder(ExprBuilderMixin, DeclBuilderMixin, StmtBuilderMixin):
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
            if new_node:
                new_node.InitializeDefaults(node)
            return new_node
        else:
            children = []
            if node.children:
                for child in node.children:
                    children.append(self.VisitParseTreeNode(child))
            new_node = ParseTreeNode(node.token, node.rule, children)
            return new_node

    def CreateCompilationUnit(self, klass, node):
        (pkg_decl, import_decls, type_decls) = self._resolve(
            node, 'PackageDeclaration', '+ImportDeclarations',
            '+TypeDeclarations')
        return klass(pkg_decl, import_decls, type_decls)

    def CreateType(self, klass, node):
        (primitive, reference) = self._resolve(
            node, 'PrimitiveType', 'ReferenceType')
        return primitive or reference[0]

    def CreateArrayType(self, klass, node):
        type_or_name = self.VisitParseTreeNode(node[0])  # Primitive or Name
        return klass(type_or_name)

    def CreateClassOrInterfaceType(self, klass, node):
        name = self.VisitParseTreeNode(node.Get('Name'))
        return klass(name.name)

    def CreatePrimitiveType(self, klass, node):
        (integral_type, boolean) = self._resolve(
            node, 'IntegralType', 'boolean')
        if boolean is not None:
            return klass(boolean.token) 
        else:
            return klass(integral_type[0].token)

    def CreateName(self, klass, node):
        if node.rule.lhs == 'Name':
            return self.CreateName(klass, node[0])  # Simple, Qualified
        elif node.rule.lhs == 'SimpleName':
            return klass([node[0].token])
        else:
            lhs = self.CreateName(klass, node[0])
            return klass(lhs.name + [node[-1].token])

    def CreateLiteral(self, klass, node):
        if node.token:  # 2147483648
            return klass(node.token)
        return klass(node[0].token)
