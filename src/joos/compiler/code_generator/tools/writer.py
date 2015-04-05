class Writer(object):
    def __init__(self, namer, output_dir, comp_unit):
        filename = "{}/{}.s".format(output_dir, namer.Visit(comp_unit))
        self.file = open(filename, 'w')
        self.indent = 0

    def Indent(self, indentation=2):
        self.indent += indentation

    def Dedent(self, indentation=2):
        self.indent -= indentation

    def OutputLine(self, string):
        self.file.write(" " * self.indent)
        self.file.write(string)
        self.file.write('\n')
