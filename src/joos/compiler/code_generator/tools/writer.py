from joos.compiler.code_generator.tools.namer import ClassOrInterfaceName


class Writer(object):
    def __init__(self, output_dir, comp_unit):
        type_decl = comp_unit.env.LookupClassOrInterface()[1]
        filename = "{}/{}.s".format(output_dir, ClassOrInterfaceName(type_decl))
        self.file = open(filename, 'w')

    def OutputLine(self, string):
        self.file.write(string)
        self.file.write('\n')

    def DefineGlobalLabel(self, label):
        self.OutputLine("global {}".format(label))
        self.OutputLine("{}:".format(label))
