from joos.errors import err


class TypeMap(object):
    def __init__(self, default=False,
                 decls=None,
                 packages=None):
        if decls is None:
            decls = {}
        if packages is None:
            packages = {}
        self.default = default
        self.decls = decls
        self.packages = packages

    def RecursiveAddNode(self, pkg_list, decl_tuple):
        (name, decl) = decl_tuple
        if pkg_list:
            first, last = pkg_list[0], pkg_list[1:]
            if first not in self.packages:
                if first in self.decls:
                    err(decl.name,
                        'Attempted to redefine type with package: ' + name)
                self.packages[first] = TypeMap()
            self.packages[first].RecursiveAddNode(last, decl_tuple)
        else:
            if name in self.decls:
                err(decl.name,
                    "Duplicate definition of " + name)
            if name in self.packages and not self.default:
                err(decl.name,
                    "Attempted to redefine package with type: " + name)
            self.decls[name] = decl

    def RecursiveLookupPackage(self, names):
        if names:
            first, last = names[0], names[1:]
            if first in self.packages:
                return self.packages[first].RecursiveLookupPackage(last)
            else:
                return None
        return self

    def RecursiveLookupType(self, names):
        if len(names) > 1:
            first, last = names[0], names[1:]
            if first in self.packages:
                return self.packages[first].RecursiveLookupType(last)
            else:
                return None
        elif len(names) == 1:
            return self.decls.get(names[0])

    def AddNode(self, node):
        pkg = node.env.LookupPackage()
        pkg = pkg and pkg[0].split('.')
        decl_tuple = node.env.LookupClassOrInterface()
        if decl_tuple is not None:
            self.RecursiveAddNode(pkg, decl_tuple)

    def LookupPackage(self, pkg):
        if not pkg:
            return self
        names = pkg.split('.')
        return self.RecursiveLookupPackage(names)

    def LookupType(self, canon_name):
        names = canon_name.split(".")
        return self.RecursiveLookupType(names)

    def __repr__(self):
        return 'Packages: {}, Decls: {}'.format(
            self.packages.keys(), self.decls.keys())
