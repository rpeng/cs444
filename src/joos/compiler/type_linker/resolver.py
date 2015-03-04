from joos.errors import err


class Resolver(object):
    def __init__(self, type_map):
        self.type_map = type_map

    def _ResolveSelfName(self, name):
        # Look in own class name
        canon = name.AsString()
        if canon == name.env.LookupClassOrInterface()[0]:
            return True
        return False

    def _ResolveClassImport(self, name):
        # Look in class imports
        canon = name.AsString()
        class_import = name.env.LookupClassImport(canon)

        if class_import is not None:
            name.linked_type = class_import[1]
            return True
        return False

    def _ResolveOwnPackage(self, name):
        # Look in own package
        canon = name.AsString()
        pkg = name.env.LookupPackage()
        pkg = self.type_map.LookupPackage(pkg and pkg[0])

        type = pkg.LookupType(canon)
        if type:
            name.linked_type = type
            return True
        return False

    def _ResolvePackageImports(self, name):
        # Look in package imports
        canon = name.AsString()
        results = name.env.LookupNameInPackages(canon)
        if results:
            if len(results) > 1:
                err(name.tokens[0], "Ambiguous usage of: " + canon)
            else:
                name.linked_type = results[0]
                return True
        return False

    def _ResolveFullyQualified(self, name):
        canon = name.AsString()
        decl = self.type_map.LookupType(canon)
        if decl is not None:
            name.linked_type = decl
            return True
        return False

    def Resolve(self, name):
        canon = name.AsString()
        if name.IsSimple():
            resolved = (self._ResolveSelfName(name) or
                        self._ResolveClassImport(name) or
                        self._ResolveOwnPackage(name) or
                        self._ResolvePackageImports(name))
        else:
            resolved = self._ResolveFullyQualified(name)
        if not resolved:
            err(name.tokens[0], "Type does not exist: " + canon)
