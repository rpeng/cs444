from .type_checker import TypeChecker


def CheckTypes(app):
    for unit in app.compilation_units:
        type_checker = TypeChecker(unit, app.type_map)
        type_checker.Start()
