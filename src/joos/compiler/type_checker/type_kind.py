class TypeKind(object):
    BOOL = 'bool'
    BYTE = 'byte'
    CHAR = 'char'
    INT = 'int'
    SHORT = 'short'
    NULL = 'null'
    VOID = 'void'
    STRING = 'string'
    REF = 'ref'

    def __init__(self, kind, decl=None):
        self.kind = kind
        self.decl = decl

    @classmethod
    def FromIntegral(cls, integral):
        int_value = int(integral)
        if -128 <= int_value <= 127:
            return cls(TypeKind.BYTE)
        elif -32768 <= int_value <= 32767:
            return cls(TypeKind.SHORT)
        elif -2147483648 <= int_value <= 2147483647:
            return cls(TypeKind.INT)

    def __repr__(self):
        return "TypeKind: kind:{} decl:{}".format(self.kind, self.decl)
