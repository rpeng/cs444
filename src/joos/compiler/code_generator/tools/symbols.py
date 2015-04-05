class Symbols(object):
    def __init__(self, writer):
        self.imported_names = set()
        self.exported_names = set()
        self.writer = writer

    def Import(self, name):
        self.imported_names.add(name)

    def Export(self, name):
        self.exported_names.add(name)

    def GenerateSymbolsSection(self):
        self.writer.OutputLine("; Symbol Exports")
        for name in self.exported_names:
            self.writer.OutputLine("global {}".format(name))
        self.writer.OutputLine("")

        self.writer.OutputLine("; Symbol Imports")
        for name in self.imported_names - self.exported_names:
            self.writer.OutputLine("extern {}".format(name))
        self.writer.OutputLine("")

    def DefineSymbolLabel(self, name):
        self.exported_names.add(name)
        self.writer.OutputLine("{}:".format(name))
