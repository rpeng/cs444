from expr import *
from stmt import *
from decl import *
from base import *


def GenerateCode(app, output_dir):
    for unit in app.compilation_units:
        code_generator = CodeGenerator(unit, app.type_map, output_dir)
        code_generator.Start()
