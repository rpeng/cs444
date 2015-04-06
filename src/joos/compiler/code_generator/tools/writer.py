from contextlib import contextmanager


class Writer(object):
    def __init__(self, filename):
        self.file = open(filename, 'w')
        self.indent = 0
        self.label_number = 0

    def Indent(self, indentation=2):
        self.indent += indentation

    def Dedent(self, indentation=2):
        self.indent -= indentation

    def OutputLine(self, string=None):
        if string:
            self.file.write(" " * self.indent)
            self.file.write(string)
        self.file.write('\n')

    def NewLabel(self, name=None):
        if name:
            label_name = "L{}_{}".format(self.label_number, name)
        else:
            label_name = "L{}"
        self.label_number += 1
        return label_name

    def OutputLabel(self, name):
        self.OutputLine("{}:".format(name))

    def LabelContext(self, name):
        self.OutputLabel(name)
        self.Indent()
        yield
        self.Dedent()

    @contextmanager
    def FunctionContext(self, indent=1):
        self.Indent(indent)
        self.OutputLine('push ebp')
        self.OutputLine('mov ebp, esp')
        yield
        self.OutputLine('leave')
        self.OutputLine('ret')
        self.OutputLine()
        self.Dedent(indent)
