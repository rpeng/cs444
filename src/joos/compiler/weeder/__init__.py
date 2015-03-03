from weeder import WeederVisitor


def WeedAST(ast, filename):
    visitor = WeederVisitor(filename)
    ast.visit(visitor)
