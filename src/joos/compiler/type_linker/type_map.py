from joos.errors import err


class TypeMap(object):
    def __init__(self):
        self.type_map = {}

    def AddNode(self, node):
        pkg = node.env.LookupPackage()
        decl_tuple = node.env.LookupClassOrInterface()
        if pkg is not None:
            pkg = pkg[0]
        else:
            pkg = ''
        if decl_tuple is not None:
            (name, decl) = decl_tuple
            if pkg not in self.type_map:
                self.type_map[pkg] = {}
            if name in self.type_map[pkg]:
                err(decl.name,
                    "Duplicate definition of " + name)
            self.type_map[pkg][name] = decl

    def LookupPackage(self, pkg):
        return self.type_map.get(pkg)

    def LookupType(self, canon_name):
        names = canon_name.split(".")
        pkg_name = ".".join(names[:-1])
        type_name = names[-1]

        pkg = self.LookupPackage(pkg_name)
        return pkg and pkg.get(type_name)

    def __repr__(self):
        return str(self.type_map)
