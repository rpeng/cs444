from joos.errors import err
from joos.syntax import ArrayType


class NameType(object):
    EXPR = 0
    TYPE = 1
    PACKAGE = 2

class Disambiguator(object):
    def __init__(self, type_map):
        self.type_map = type_map

    def CheckLocalVars(self, name, env):
        decl = env.LookupLocalVar(name)
        if decl is not None:
            return (NameType.EXPR, decl.l_type)

    def CheckParams(self, name, env):
        decl = env.LookupParameter(name)
        if decl is not None:
            return (NameType.EXPR, decl.p_type)

    def CheckFields(self, name, env):
        decl = env.LookupField(name)
        if decl is ArrayType.LengthDecl:
            return (NameType.EXPR, decl)
        elif decl is not None:
            return (NameType.EXPR, decl.f_type)

    def CheckClassImport(self, name, env):
        decl = env.LookupClassImport(name)
        if decl is not None:
            return (NameType.TYPE, decl)

    def CheckOwnPackage(self, name, env):
        type_map = env.VisibleTypes()
        decl = type_map.LookupType(name)
        if decl is not None:
            return (NameType.TYPE, decl)

    def CheckPackageImport(self, name, env):
        decl = env.LookupNameInPackages(name)
        if decl is not None:
            return (NameType.TYPE, decl)

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

    def DisambiguateAndLink(self, node):
        first = node.Split()[0]
        env = node.env
        result = self.CheckNameAndEnv(first, env)

        if result:
            name_type, decl_or_pkg = result
            for name in node.Split()[1:]:
                if decl_or_pkg is None:
                    err(node.tokens[0], "Name " + node.AsString() + " not found.")
                if name_type == NameType.PACKAGE:
                    next = (self.CheckTypeInPackage(name, decl_or_pkg) or
                            self.CheckPackageInPackage(name, decl_or_pkg))
                elif name_type == NameType.TYPE or name_type == NameType.EXPR:
                    if isinstance(decl_or_pkg, ArrayType):
                        if name == 'length':
                            next = (NameType.TYPE, ArrayType.LengthDecl)
                    else:
                        next = (self.CheckFields(name, decl_or_pkg.env))
                if not next:
                    err(node.tokens[0], "Name " + node.AsString() + " not found.")
                name_type, decl_or_pkg = next
        else:
            err(node.tokens[0], "Name " + node.AsString() + " not found.")

        if name_type == NameType.PACKAGE:
            err(node.tokens[0], "Unexpected package")
