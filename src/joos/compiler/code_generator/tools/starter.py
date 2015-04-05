from .namer import Namer
from .symbols import Symbols
from .writer import Writer


class Starter(object):
    def __init__(self, app, output_dir):
        self.app = app
        self.writer = Writer("{}/__main.s".format(output_dir))
        self.namer = Namer()
        self.symbols = Symbols(self.writer)



    def GenerateStartScript(self):
        self.writer.OutputLine("; Program entry point")
        self.writer.OutputLine()

        start_symbol = "ms~{}~test".format(
            self.namer.Visit(self.app.compilation_units[0]))
        self.symbols.Import(start_symbol)

        self.writer.OutputLine("section .text")
        self.symbols.DefineSymbolLabel("_start")
        self.writer.Indent()

        self.writer.OutputLine("; static initialization")
        for unit in self.app.compilation_units:
            init_name = "is~{}".format(self.namer.Visit(unit))
            self.symbols.Import(init_name)
            self.writer.OutputLine("call {}".format(init_name))

        self.writer.OutputLine("; Main entry point")
        self.writer.OutputLine("call {}".format(start_symbol))
        self.writer.OutputLine("mov ebx, eax")
        self.writer.OutputLine("mov eax, 1")
        self.writer.OutputLine("int 0x80")

        self.writer.Dedent()
        self.writer.OutputLine()

        self.symbols.GenerateSymbolsSection()
