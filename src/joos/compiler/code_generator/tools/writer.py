class Writer(object):
    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.indent = 0

    def Indent(self, indentation=2):
        self.indent += indentation

    def Dedent(self, indentation=2):
        self.indent -= indentation

    def OutputLine(self, string=None):
        if string:
            self.file.write(" " * self.indent)
            self.file.write(string)
        self.file.write('\n')
