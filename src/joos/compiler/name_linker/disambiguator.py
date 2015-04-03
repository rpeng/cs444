from joos.errors import err
from joos.syntax import *


class NameType(object):
    EXPR = 0
    TYPE = 1
    PACKAGE = 2

class Disambiguator(object):
    def __init__(self, type_map):
        self.type_map = type_map

    def TypeToDecl(self, type):
        if isinstance(type, ClassOrInterfaceType):
            return type.name.linked_type
        return type

    def CheckLocalVars(self, name, env):
        decl = env.LookupLocalVar(name)
        if decl:
            return (NameType.EXPR, self.TypeToDecl(decl.l_type))

    def CheckParams(self, name, env):
        decl = env.LookupParameter(name)
        if decl:
            return (NameType.EXPR, self.TypeToDecl(decl.p_type))

    def CheckFields(self, name, env):
        decl = env.LookupField(name)
        if decl is ArrayType.LengthDecl:

            return (NameType.EXPR, decl)
        elif decl:
            return (NameType.EXPR, self.TypeToDecl(decl.f_type))

    def CheckClassImport(self, name, env):
        decl = env.LookupClassImport(name)
        if decl:
            return (NameType.TYPE, decl[1])

    def CheckOwnPackage(self, name, env):
        type_map = env.VisibleTypes()
        decl = type_map.LookupType(name)
        if decl:
            return (NameType.TYPE, decl)

    def CheckPackageImport(self, name, env):
        decl = env.LookupNameInPackages(name)
        if decl:
            return (NameType.TYPE, decl[0])

    def CheckPackage(self, name, env):
        pkg = self.type_map.LookupPackage(name)
        if pkg:
            return (NameType.PACKAGE, pkg)

    def CheckTypeInPackage(self, name, pkg):
        decl = pkg.LookupType(name)
        if decl:
            return (NameType.TYPE, decl)

    def CheckPackageInPackage(self, name, pkg):
        new_pkg = pkg.LookupPackage(name)
        if new_pkg:
            return (NameType.PACKAGE, new_pkg)

    def CheckNameAndEnv(self, name, env):
        return (self.CheckLocalVars(name, env) or
                self.CheckParams(name, env) or
                self.CheckFields(name, env) or
                self.CheckClassImport(name, env) or
                self.CheckOwnPackage(name, env) or
                self.CheckPackageImport(name, env) or
                self.CheckPackage(name, env))

    def DisambiguateAndLinkMethod(self, node):
        tokens = node.name.Split()
        prefix = tokens[:-1]
        if prefix:
            self.DisambiguateAndLink(node.name, prefix)
        else:
            node.name.linked_type = node.env.LookupClassOrInterface()[1]
            node.name.linked_decl = node.name.linked_type
        node.linked_decl = node.name.linked_type

    def DisambiguateAndLink(self, node, name_tokens=None):
        tokens = name_tokens
        if not name_tokens:
            tokens = node.Split()
        first = tokens[0]
        env = node.env
        result = self.CheckNameAndEnv(first, env)

        if result:
            name_type, decl_or_pkg = result
            for name in tokens[1:]:
                if decl_or_pkg is None:
                    err(node.tokens[0], "Name " + node.AsString() + " not found.")
                if name_type == NameType.PACKAGE:
                    next = (self.CheckTypeInPackage(name, decl_or_pkg) or
                            self.CheckPackageInPackage(name, decl_or_pkg))
                elif name_type == NameType.TYPE or name_type == NameType.EXPR:
                    if isinstance(decl_or_pkg, ArrayType):
                        if name == 'length':
                            next = (NameType.TYPE, ArrayType.LengthDecl)
                    elif isinstance(decl_or_pkg, PrimitiveType):
                        err(node.tokens[0], "Cannot dereference primitive type")
                    else:
                        next = (self.CheckFields(name, decl_or_pkg.env))
                if not next:
                    err(node.tokens[0], "Name " + node.AsString() + " not found.")
                name_type, decl_or_pkg = next
            if name_type == NameType.PACKAGE:
                err(node.tokens[0], "Unexpected package")
            node.name_type = name_type
            node.linked_type = decl_or_pkg
        else:
            err(node.tokens[0], "Name " + node.AsString() + " not found.")

