from joos.errors import err
from joos.syntax import ArrayType, ClassOrInterfaceType


class AccessContext(object):
    EXPR = 0  # local var / field
    CLASS = 1  # Class.
    PKG = 2  # some package
    PRIM = 3  # Primitive type

    def __init__(self, type, decl, parent_type=None, linked=None):
        self.type = type
        self.decl = decl
        self.parent_type = parent_type
        self.linked = linked


class AccessError(Exception):
    pass


class AccessChecker(object):
    def __init__(self, type_map):
        self.type_map = type_map

    def TypeToDecl(self, type):
        if isinstance(type, ClassOrInterfaceType):
            return type.name.linked_type
        return type

    def CanAccessProtected(self, context, declared, static=False):
        other_class = context.decl.env.LookupClassOrInterface()[1]

        # OK if we are in same package
        own_pkg = context.parent_type.env.LookupPackage()

        if own_pkg is not None:
            own_pkg = own_pkg[1]

        env_pkg = other_class.env.LookupPackage()
        if env_pkg is not None:
            env_pkg = env_pkg[1]

        if env_pkg == own_pkg:
            return True

        # Not OK if we are not a subclass of declared
        declared_class = declared.env.LookupClassOrInterface()[1]
        if declared_class not in context.parent_type.linked_supers:
            return False

        # OK if we are in the parent class, and we are a subclass of other
        if not static and context.parent_type in other_class.linked_supers:
            return True

        # if static, OK if we are subclass of declared class
        if static and other_class in context.parent_type.linked_supers:
            return True

        return False

    def CheckProtectedAccess(self, context, declared, static=False):
        if not self.CanAccessProtected(context, declared, static):
            raise AccessError("Access in protected context")

    def CheckLocalVars(self, name, context):
        env = context.decl.env
        decl = env.LookupLocalVar(name)
        if decl:
            return (AccessContext.EXPR, self.TypeToDecl(decl.l_type), decl)

    def CheckParams(self, name, context):
        env = context.decl.env
        decl = env.LookupParameter(name)
        if decl:
            return (AccessContext.EXPR, self.TypeToDecl(decl.p_type), decl)

    def CheckFields(self, name, context):
        env = context.decl.env

        if isinstance(context.decl, ArrayType):
            if name == 'length':
                return (AccessContext.PRIM, ArrayType.LengthDecl)

        decl = env.LookupField(name)
        if decl is ArrayType.LengthDecl:
            return (AccessContext.EXPR, decl, decl)
        elif decl:
            if (context.type == AccessContext.CLASS and not decl.IsStatic()):
                raise AccessError("Access of non-static field in static context")
            if (context.type == AccessContext.EXPR and decl.IsStatic()):
                raise AccessError("Access of static field in non-static context")

            if decl.IsProtected():
                if decl.IsStatic():
                    context.decl = decl
                self.CheckProtectedAccess(context, decl, decl.IsStatic())
            return (AccessContext.EXPR, self.TypeToDecl(decl.f_type), decl)

    def CheckClassImport(self, name, context):
        env = context.decl.env
        decl = env.LookupClassImport(name)
        if decl:
            return (AccessContext.CLASS, decl[1], decl)

    def CheckOwnPackage(self, name, context):
        env = context.decl.env
        type_map = env.VisibleTypes()
        decl = type_map.LookupType(name)
        if decl:
            return (AccessContext.CLASS, decl, decl)

    def CheckPackageImport(self, name, context):
        env = context.decl.env
        decl = env.LookupNameInPackages(name)
        if decl:
            return (AccessContext.CLASS, decl[0], decl)

    def CheckPackage(self, name, context):
        pkg = self.type_map.LookupPackage(name)
        if pkg:
            return (AccessContext.PKG, pkg, pkg)

    def CheckTypeInPackage(self, name, context):
        decl = context.decl.LookupType(name)
        if decl:
            return (AccessContext.CLASS, decl, decl)

    def CheckPackageInPackage(self, name, context):
        new_pkg = context.decl.LookupPackage(name)
        if new_pkg:
            return (AccessContext.PKG, new_pkg, new_pkg)

    def CheckAll(self, name, context):
        return (self.CheckLocalVars(name, context) or
                self.CheckParams(name, context) or
                self.CheckFields(name, context) or
                self.CheckClassImport(name, context) or
                self.CheckOwnPackage(name, context) or
                self.CheckPackageImport(name, context) or
                self.CheckPackage(name, context))

    def CheckInPackage(self, name, context):
        return (self.CheckTypeInPackage(name, context) or
                self.CheckPackageInPackage(name, context))

    def CheckAccess(self, debug_token, names, context):
        if not names:
            return None

        for current in names:
            try:
                if context.type == AccessContext.PKG:
                    (type, decl, linked) = self.CheckInPackage(current, context)
                else:
                    (type, decl, linked) = self.CheckAll(current, context)
                context = AccessContext(type, decl, context.parent_type, linked)
            except AccessError, e:
                err(debug_token, e.message)
        return context

    # Entry Points
    def CheckName(self, node, is_static):
        tokens = node.Split()
        parent = node.env.LookupClassOrInterface()[1]
        if is_static:
            context = AccessContext(AccessContext.CLASS, node, parent)
        else:
            context = AccessContext(AccessContext.EXPR, node, parent)
        node.context = self.CheckAccess(node.tokens[0], tokens, context)


    def CheckConstructor(self, node):
        if node.linked_type.IsProtected():
            own_pkg = node.env.LookupPackage()
            other_pkg = node.linked_type.env.LookupPackage()
            if own_pkg is None or other_pkg is None:
                if own_pkg != other_pkg:
                    err(node[0].token, "Access of protected constructor")
            elif own_pkg[1] != other_pkg[1]:
                err(node[0].token, "Access of protected constructor")


    def CheckMethodName(self, node, is_static):
        tokens = node.name.Split()
        parent = node.env.LookupClassOrInterface()[1]

        if is_static:
            context = AccessContext(AccessContext.CLASS, node, parent)
        else:
            context = AccessContext(AccessContext.EXPR, node, parent)
        context = self.CheckAccess(node[1].token, tokens[:-1], context)

        if (context.type == AccessContext.CLASS and not node.linked_method.IsStatic()):
            err(node[1].token, "Access of non-static method in static context")
        if (context.type == AccessContext.EXPR and node.linked_method.IsStatic()):
            err(node[1].token, "Access of static method in non-static context")

        if node.linked_method.IsStatic():
            context.decl = node.linked_method.env.LookupClassOrInterface()[1]

        if node.linked_method.IsProtected():
            if not self.CanAccessProtected(
                    context,
                    node.linked_method,
                    static=node.linked_method.IsStatic()):
                err(node[1].token, "Access of protected method")

        node.context = context



