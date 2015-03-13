import collections

from joos.errors import err


class Environment(object):
    def __init__(self, upstream=None):
        self.package = None  # (name, PackageDecl)
        self.class_or_interface = None  # (name, ClassOrInterfaceDecl)
        self.fields = collections.OrderedDict()  # (name -> FieldDecl)
        self.methods = collections.defaultdict(list)  # (name -> MethodDecl[])
        self.parameters = {}  # (name -> Parameter)
        self.local_vars = {}  # (name -> LocalVariableDecl)

        self.inherited_env = None
        self.type_map = None
        self.class_imports = {}  # (name -> (name_node, ClassOrInterfaceDecl))
        self.package_imports = {}  # (name -> type_map[name])
        self.upstream = upstream

    @classmethod
    def Empty(cls):
        return cls()

    def Fork(self):
        return Environment(self)

    def VisibleTypes(self):
        pkg = self.LookupPackage()
        type_map = self.LookupTypeMap()
        if pkg:
            return type_map.LookupPackage(pkg[0])
        return type_map

    def LookupInherited(self):
        if self.inherited_env is not None:
            return self.inherited_env
        if self.upstream is not None:
            return self.upstream.LookupInherited()

    def LookupTypeMap(self):
        if self.type_map is not None:
            return self.type_map
        if self.upstream is not None:
            return self.upstream.LookupTypeMap()

    def LookupClassOrInterface(self):
        if self.class_or_interface is not None:
            return self.class_or_interface
        if self.upstream is not None:
            return self.upstream.LookupClassOrInterface()

    def LookupPackage(self):
        if self.package is not None:
            return self.package
        if self.upstream is not None:
            return self.upstream.LookupPackage()

    def LookupField(self, name):
        if name in self.fields:
            return self.fields[name]
        if self.upstream is not None:
            field = self.upstream.LookupField(name)
            if field is not None:
                return field
        inherited = self.LookupInherited()
        if inherited is not None:
            return inherited.LookupField(name)

    def FieldIndex(self, name):
        if not self.fields:
            if self.upstream:
                return self.upstream.FieldIndex(name)
        else:
            if name in self.fields:
                return self.fields.keys().index(name)

    def LookupMethod(self, name):
        if name in self.methods:
            return self.methods[name]
        if self.upstream is not None:
            return self.upstream.LookupMethod(name)

    def LookupParameter(self, name):
        if name in self.parameters:
            return self.parameters[name]
        if self.upstream is not None:
            return self.upstream.LookupParameter(name)

    def LookupLocalVar(self, name):
        if name in self.local_vars:
            return self.local_vars[name]
        if self.upstream is not None:
            return self.upstream.LookupLocalVar(name)

    def LookupClassImport(self, name):
        if name in self.class_imports:
            return self.class_imports[name]
        if self.upstream is not None:
            return self.upstream.LookupClassImport(name)

    def LookupNameInPackages(self, name):
        if not self.package_imports:
            if self.upstream is not None:
                return self.upstream.LookupNameInPackages(name)
            else:
                return None

        results = []
        for type_map in self.package_imports.values():
            type = type_map.LookupType(name)
            if type:
                results.append(type)
        return results

    def Update(self, update_env):
        if update_env.upstream is not None:
            self.Update(update_env.upstream)
        if update_env.package:
            self.package = update_env.package
        if update_env.class_or_interface:
            self.class_or_interface = update_env.class_or_interface
        for field, value in update_env.fields.items():
            self.AddField(field, value)
        for name, nodes in update_env.methods.items():
            for node in nodes:
                self.AddMethod(name, node)
        for name, node in update_env.parameters.items():
            self.AddParameter(name, node)
        for name, node in update_env.local_vars.items():
            self.AddLocalVar(name, node)
        for name, (node, decl) in update_env.class_imports.items():
            self.AddClassImport(node, decl)
        for name, pkg in update_env.package_imports.items():
            self.AddPackageImport(name, pkg)

    def AddPackage(self, name, node):
        self.package = (name, node)

    def AddTypeMap(self, type_map):
        self.type_map = type_map

    def AddClassOrInterface(self, name, node):
        self.class_or_interface = (name, node)

    def AddField(self, name, node):
        if self.LookupField(name) is not None:
            err(node.var_decl.var_id, "Duplicate field name: " + name)
        self.fields[name] = node

    def AddMethod(self, name, node):
        self.methods[name].append(node)

    def AddParameter(self, name, node):
        if self.LookupParameter(name) is not None:
            err(node.var_id, "Duplicate parameter: " + name)
        self.parameters[name] = node

    def AddLocalVar(self, name, node):
        if (self.LookupLocalVar(name) is not None or
                self.LookupParameter(name) is not None):
            err(node.var_decl.var_id,
                "Duplicate variable in overlapping scope: " + name)
        self.local_vars[name] = node

    def AddInherited(self, env):
        self.inherited_env = env

    def AddClassImport(self, node, decl):
        # node : Name
        name = node.Last()
        type = self.LookupClassOrInterface()
        if type is not None and name == type[0]:
            pkg = self.LookupPackage()
            decl = self.LookupClassOrInterface()
            if pkg and decl:
                pkg = pkg[0]
                decl = decl[0]
            # You are allowed to import yourself
            if not (node.Prefix() == pkg and node.Last() == decl):
                err(node.tokens[0], "Import clashes with class decl: " + name)
        class_import = self.LookupClassImport(name)
        if class_import is not None:
            class_name = class_import[0]
            # You can include the same thing twice
            if node.AsString() != class_name.AsString():
                err(node.tokens[0], "Import clashes with another: " + name)
        self.class_imports[name] = (node, decl)

    def AddPackageImport(self, name, pkg):
        self.package_imports[name] = pkg

    def _join(self):
        if self.upstream:
            (pkg, type, fields, methods, params, vars,
             class_imports, pkg_imports) = self.upstream._join()
            return (self.package and self.package[0] or pkg,
                    self.class_or_interface or type,
                    self.fields.keys() + fields,
                    self.methods.keys() + methods,
                    self.parameters.keys() + params,
                    self.local_vars.keys() + vars,
                    self.class_imports.keys() + class_imports,
                    self.package_imports.keys() + pkg_imports)
        else:
            return (self.package and self.package[0],
                    self.class_or_interface and self.class_or_interface[0],
                    self.fields.keys(),
                    self.methods.keys(),
                    self.parameters.keys(),
                    self.local_vars.keys(),
                    self.class_imports.keys(),
                    self.package_imports.keys())

    def __repr__(self):
        (pkg, type, fields, methods,
         params, vars, class_imports, pkg_imports) = self._join()
        return """Environment:
  package: {pkg}
  type: {type}
  fields: {fields}
  methods: {methods}
  params: {params}
  vars: {vars}
  class imports: {class_imports}
  pkg imports: {pkg_imports}
""".format(pkg=pkg,
           type=type,
           fields=', '.join(fields),
           methods=', '.join(methods),
           params=', '.join(params),
           vars=', '.join(vars),
           class_imports=', '.join(class_imports),
           pkg_imports=', '.join(pkg_imports))
