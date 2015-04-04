from joos.compiler.environment import Environment


class StmtCodeMixin(object):
    # Statement
    def VisitBlock(self, node):
        raise NotImplementedError

    def VisitIfThenElseStatement(self, node):
        raise NotImplementedError

    def VisitWhileStatement(self, node):
        raise NotImplementedError

    def VisitForStatement(self, node):
        raise NotImplementedError

    def VisitReturnStatement(self, node):
        raise NotImplementedError

    def VisitEmptyStatement(self, node):
        raise NotImplementedError
