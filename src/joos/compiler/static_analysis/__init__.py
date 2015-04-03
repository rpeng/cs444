from joos.compiler.static_analysis.analyzer import StaticAnalyzer


def StaticallyAnalyze(app):
    for unit in app.compilation_units:
        static_analyzer = StaticAnalyzer(unit, app.type_map)
        static_analyzer.Start()
