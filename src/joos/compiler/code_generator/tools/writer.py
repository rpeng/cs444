from contextlib import contextmanager


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

    @contextmanager
    def FunctionContext(self):
        self.Indent()
        self.OutputLine('push ebp')
        self.OutputLine('mov ebp, esp')
        yield
        self.OutputLine('leave')
        self.OutputLine('ret')
        self.OutputLine()
        self.Dedent()
