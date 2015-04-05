from joos.syntax import Type, PrimitiveType, ClassOrInterfaceType, ASTVisitor, Name

METHOD_PREFIX = 'm'
STATIC_METHOD_PREFIX = 'ms'
CONSTRUCTOR_PREFIX = 'mc'

PRIMITIVE_MAP = {
    'int': '@int',
    'bool': '@bool',
    'byte': '@byte',
    'char': '@char',
    'short': '@short'
}

class Namer(ASTVisitor):
    def DefaultBehaviour(self, node):
        raise NotImplementedError

    def GetTypeName(self, node):
        pkg = node.env.LookupPackage()
        type_name =  node.env.LookupClassOrInterface()[0]
        if pkg:
            return "{}.{}".format(pkg[0], type_name)
        else:
            return type_name

    def VisitCompilationUnit(self, node):
        return self.GetTypeName(node)

    def VisitClassDecl(self, node):
        return self.GetTypeName(node)

    def VisitInterfaceDecl(self, node):
        return self.GetTypeName(node)

    def VisitClassOrInterfaceType(self, node):
        return self.Visit(node.name.linked_type)

    def VisitPrimitiveType(self, node):
        return PRIMITIVE_MAP[node.t_type.token_type]

    def VisitArrayType(self, node):
        if isinstance(node.type_or_name, Name):
            element_type = self.Visit(node.type_or_name.linked_type)
        else:
            element_type = self.Visit(node.type_or_name)
        return "${}".format(element_type)

    def VisitParameter(self, node):
        return self.Visit(node.p_type)

    def VisitMethodDecl(self, node):
        if node.IsStatic():
            prefix = STATIC_METHOD_PREFIX
        else:
            prefix = METHOD_PREFIX

        type_name = self.GetTypeName(node)
        method_name = node.header.m_id.lexeme

        args = []
        if node.header.params:
            for param in node.header.params:
                args.append(self.Visit(param))


        if args:
            return "{}~{}~{}~{}".format(prefix, type_name,
                                        method_name, "~".join(args))
        else:
            return "{}~{}~{}".format(prefix, type_name, method_name)

    def VisitConstructorDecl(self, node):
        type_name = self.GetTypeName(node)

        args = []
        if node.params:
            for param in node.params:
                args.append(self.Visit(param))
        if args:
            return "{}~{}~{}".format(CONSTRUCTOR_PREFIX, type_name, "~".join(args))
        else:
            return "{}~{}".format(CONSTRUCTOR_PREFIX, type_name)


