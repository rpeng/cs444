def _err(token, msg):
    string = "Row {} col {}: {}".format(token.row, token.col, msg)
    raise RuntimeError(string)


class Environment(object):
    def __init__(self, upstream=None):
        self.fields = {}  # (name, FieldDecl)
        self.methods = {}  # (name, MethodDecl)
        self.packages = {}  # (name, PackageDecl) 
        self.local_vars = {}  # (name, LocalVariableDecl)

        self.upstream = upstream

    def Fork(self):
        return Environment(self)

    def LookupField(name):
        if name in self.fields:
            return self.fields[name]
        elif upstream is not None:
            return self.upstream.LookupField(name)
        else:
            return None

    def LookupMethod(name):
        if name in self.methods:
            return self.methods[name]
        elif upstream is not None:
            return self.upstream.LookupMethod(name)
        else:
            return None

    def LookupPackage(name):
        if name in self.packages:
            return self.packages[name]
        elif upstream is not None:
            return self.upstream.LookupPackages(name)
        else:
            return None

    def LookupLocalVar(name):
        if name in self.local_vars:
            return self.local_vars[name]
        elif upstream is not None:
            return self.upstream.LookupLocalVar(name)
        else:
            return None
    
    def AddField(name, value):
        self.fields[name] = value
