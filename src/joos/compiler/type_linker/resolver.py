from joos.errors import err


class Resolver(object):
    def __init__(self, type_map):
        self.type_map = type_map

    def _CheckPrefix(self, canon, name):
        split = canon.split('.')

        for i in range(1, len(split)):
            prefix = '.'.join(split[:i])
            if self._ResolveCanon(prefix, name):
                err(name.tokens[0],
                        "Prefix of qualified type should "
                        "not resolve to a type: " + canon +
                        ' prefix: ' + prefix)

    def _ResolveSelfName(self, canon, name):
        # Look in own class name
        decl_pair = name.env.LookupClassOrInterface()
        if decl_pair:
            (decl_name, decl) = decl_pair
            if canon == decl_name:
                return decl

    def _ResolveClassImport(self, canon, name):
        # Look in class imports
        class_import = name.env.LookupClassImport(canon)
        if class_import is not None:
            return class_import[1]

    def _ResolveOwnPackage(self, canon, name):
        # Look in own package
        pkg = name.env.LookupPackage()
        pkg = self.type_map.LookupPackage(pkg and pkg[0])
        return pkg.LookupType(canon)

    def _ResolvePackageImports(self, canon, name):
        # Look in package imports
        results = name.env.LookupNameInPackages(canon)
        if results:
            if len(results) > 1:
                err(name.tokens[0], "Ambiguous usage of: " + canon)
            else:
                return results[0]

    def _ResolveFullyQualified(self, canon, name):
        self._CheckPrefix(canon, name)
        return self.type_map.LookupType(canon)

    def _ResolveCanon(self, canon, name):
        names = canon.split('.')
        if len(names) == 1:
            return (self._ResolveSelfName(canon, name) or
                    self._ResolveClassImport(canon, name) or
                    self._ResolveOwnPackage(canon, name) or
                    self._ResolvePackageImports(canon, name))
        else:
            return self._ResolveFullyQualified(canon, name)

    def Resolve(self, name):
        canon = name.AsString()
        resolved = self._ResolveCanon(canon, name)
        if resolved:
            name.linked_type = resolved
        else:
            err(name.tokens[0], "Type does not exist: " + canon)
