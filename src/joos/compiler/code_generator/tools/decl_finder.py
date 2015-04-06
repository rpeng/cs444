from joos.compiler.code_generator import Vars
from joos.compiler.name_linker.disambiguator import NameType
from joos.syntax import ClassOrInterfaceType, ArrayType


class DeclFinder(object):
    def __init__(self, namer, symbols, writer, type_map):
        self.namer = namer
        self.symbols = symbols
        self.writer = writer
        self.vars = None
        self.type_map = type_map

    def TypeToDecl(self, type):
        if isinstance(type, ClassOrInterfaceType):
            return type.name.linked_type
        return type

    def CheckLocalVars(self, name, env):
        decl = env.LookupLocalVar(name)
        if decl:
            offset = self.vars.GetLocalVarOffset(decl)
            self.writer.OutputLine("mov eax, [ebp - {}]".format(offset))
            self.writer.OutputLine("lea ebx, [ebp - {}]".format(offset))
            return (NameType.EXPR, self.TypeToDecl(decl.l_type))

    def CheckParams(self, name, env):
        decl = env.LookupParameter(name)
        if decl:
            offset = self.vars.GetParamOffset(decl)
            self.writer.OutputLine("mov eax, [ebp + {}]".format(offset))
            self.writer.OutputLine("lea ebx, [ebp + {}]".format(offset))
            return (NameType.EXPR, self.TypeToDecl(decl.p_type))

    def CheckFields(self, name, env):
        decl = env.LookupField(name)
        if decl is ArrayType.LengthDecl:
            raise NotImplementedError
        elif decl:
            if decl.IsStatic():
                static_name = self.namer.Visit(decl)
                self.symbols.Import(static_name)
                self.writer.OutputLine("mov eax, [{}]".format(static_name))
                self.writer.OutputLine("lea ebx, [{}]".format(static_name))
            else:
                offset = Vars.GetFieldOffset(decl)
                self.writer.OutputLine("add eax, {}".format(offset))
                self.writer.OutputLine("lea ebx, [eax]")
                self.writer.OutputLine("mov eax, [eax]")
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

    def CheckArrayLength(self):
        self.writer.OutputLine("mov eax, [eax + 4]")

    def ResolveName(self, node, vars, skip_last=False):
        # Eventually loads value to eax, location to ebx
        self.vars = vars

        names = node.Split()
        if skip_last:
            names = names[:-1]
        env = node.env

        self.writer.OutputLine('; loading name {}'.format(node.AsString()))
        self.writer.OutputLine('mov eax, [ebp + 8]')  # move 'this' as starting point

        type = None
        decl = None
        for name in names:
            self.writer.OutputLine('; load subname {}'.format(name))
            if type is None:
                (type, decl) = self.CheckNameAndEnv(name, env)
            elif type == NameType.TYPE or type == NameType.EXPR:
                if isinstance(decl, ArrayType) and name == 'length':
                    self.CheckArrayLength()
                else:
                    (type, decl) = self.CheckFields(name, decl.env)
            elif type == NameType.PACKAGE:
                (type, decl) = (self.CheckTypeInPackage(name, decl) or
                                self.CheckPackageInPackage(name, decl))

        self.writer.OutputLine('; loaded name {}'.format(node.AsString()))
        self.vars = None
