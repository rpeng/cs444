from joos.compiler.hierarchy_check.common import GetObject
from .namer import Namer, PRIMITIVE_MAP
from .symbols import Symbols
from .writer import Writer


class Starter(object):
    def __init__(self, app, output_dir):
        self.app = app
        self.writer = Writer("{}/__main.s".format(output_dir))
        self.namer = Namer()
        self.symbols = Symbols(self.writer)


    def OutputArrayInstanceCreator(self):
        creator_label = "new~$"

        self.writer.OutputLine("; Array Instance creator")
        self.symbols.DefineSymbolLabel(creator_label)
        self.writer.Indent()

        with self.writer.FunctionContext():
            self.writer.OutputLine('push ecx')
            self.writer.OutputLine('push edx')

            self.writer.OutputLine('push eax')  # size

            self.symbols.Import("__malloc")
            self.writer.OutputLine("lea eax, [eax * 4 + 8]")
            self.writer.OutputLine("call __malloc")

            # Copy in size
            self.writer.OutputLine('pop ebx')  # ebx has our size
            self.writer.OutputLine('mov [eax + 4], ebx')  # copy size into array

            self.writer.OutputLine('pop edx')
            self.writer.OutputLine('pop ecx')

        # User needs to copy in the vtable
        self.writer.Dedent()
        self.writer.OutputLine()

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

        self.OutputArrayInstanceCreator()

        self.writer.OutputLine("section .data")
        self.writer.OutputLine("; primitive array vtables")
        obj_label = 0
        obj_decl = GetObject()
        if obj_decl:
            obj_label = "V~{}".format(self.namer.Visit(GetObject()))
            self.symbols.Import(obj_label)

        for primitive in PRIMITIVE_MAP.values():
            label = "V~${}".format(primitive)
            self.symbols.DefineSymbolLabel(label)
            self.writer.Indent()
            self.writer.OutputLine("dd {}".format(obj_label))
            if obj_decl:
                for decl in obj_decl.ordered_methods.values():
                    if not decl.IsStatic():
                        decl_name = self.namer.Visit(decl)
                        self.symbols.Import(decl_name)
                        self.writer.OutputLine("dd {}".format(decl_name))
            self.writer.Dedent()
            self.writer.OutputLine()

        self.writer.OutputLine()
        self.symbols.GenerateSymbolsSection()
