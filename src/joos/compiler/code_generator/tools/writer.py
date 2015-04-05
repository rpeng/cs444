class Writer(object):
    def __init__(self, namer, output_dir, comp_unit):
        filename = "{}/{}.s".format(output_dir, namer.Visit(comp_unit))
        self.file = open(filename, 'w')

    def OutputLine(self, string):
        self.file.write(string)
        self.file.write('\n')

    def DefineGlobalLabel(self, label):
        self.OutputLine("global {}".format(label))
        self.OutputLine("{}:".format(label))
