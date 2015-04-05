from .namer import Namer
from .symbols import Symbols
from .writer import Writer


def GenerateStartScript(comp_unit, output_dir):
    writer = Writer("{}/__main.s".format(output_dir))
    namer = Namer()
    symbols = Symbols(writer)

    writer.OutputLine("; Program entry point")
    writer.OutputLine()

    start_symbol = "ms~{}~test".format(namer.Visit(comp_unit))
    symbols.Import(start_symbol)

    writer.OutputLine("section .text")
    symbols.DefineSymbolLabel("_start")
    writer.Indent()

    writer.OutputLine("; TODO: static initialization")

    writer.OutputLine("call {}".format(start_symbol))
    writer.OutputLine("mov ebx, eax")
    writer.OutputLine("mov eax, 1")
    writer.OutputLine("int 0x80")

    writer.Dedent()
    writer.OutputLine()

    symbols.GenerateSymbolsSection()
