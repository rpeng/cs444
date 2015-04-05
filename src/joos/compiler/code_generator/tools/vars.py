# Keeps track of local vars, and parameters on stack inside of a block

class Vars(object):
    def __init__(self,
                 writer,
                 locals=None,
                 params=None,
                 offset=0,
                 parent=None):
        self.writer = writer
        self.locals = locals or {}  # LocalVarDecl -> offset
        self.params = params or {}  # Parameter -> offset
        self.offset = offset  # in words
        self.parent = parent

    def NewBlock(self):
        self.writer.OutputLine('; begin of block')
        self.writer.Indent()
        return Vars(self.writer,
                    locals=None,
                    params=self.params,
                    offset=self.offset,
                    parent=self)

    def EndBlock(self):
        # Clean up stack
        self.writer.Dedent()
        if len(self.locals) > 0:
            self.writer.OutputLine(
                'add esp, {}'.format(len(self.locals)*4))
        self.writer.OutputLine('; end of block')
        return self.parent

    def Push(self, times=1):
        self.offset += times

    def Pop(self, times=1):
        self.offset -= times

    def AddLocalVar(self, decl):
        # Puts value of eax into local variable decl
        self.writer.OutputLine('; local var declared')
        self.writer.OutputLine('push eax')
        self.offset += 1
        self.locals[decl] = self.offset

    def AddParams(self, decls, static_method=False):
        if static_method:
            this_offset = 0
        else:
            this_offset = 1

        if decls is not None:
            n = len(decls)
            for (i, decl) in enumerate(decls):
                self.params[decl] = n + 1 + this_offset - i

    def GetParamOffset(self, decl):
        return self.params.get(decl) * 4

    def GetLocalVarOffset(self, decl):
        offset = self.locals.get(decl)
        if not offset and self.parent:
            return self.parent.GetLocalVarOffset(decl)
        return offset * 4
