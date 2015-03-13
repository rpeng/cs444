from joos.compiler.name_linker.name_linker import NameLinker


def LinkNames(app):
    for unit in app.compilation_units:
        name_linker = NameLinker(unit, app.type_map)
        name_linker.Start()
