from joos.syntax import Type


class TypeKind(object):
    BOOL = 'bool'
    BYTE = 'byte'
    CHAR = 'char'
    INT = 'int'
    SHORT = 'short'
    NULL = 'null'
    VOID = 'void'
    REF = 'ref'
    ARRAY = 'array'

    numerics = [BYTE, CHAR, SHORT, INT]
    references = [NULL, REF, ARRAY]

    def __init__(self, kind, context=None):
        self.kind = kind
        self.context = context

    @classmethod
    def FromIntegral(cls, integral):
        return cls(TypeKind.INT)

    @classmethod
    def FromIntegralImplicit(cls, integral):
        int_value = int(integral)
        if -128 <= int_value <= 127:
            return cls(TypeKind.BYTE)
        elif -32768 <= int_value <= 32767:
            return cls(TypeKind.SHORT)
        elif -2147483648 <= int_value <= 2147483647:
            return cls(TypeKind.INT)

    def IsNumeric(self):
        return self.kind in TypeKind.numerics

    def IsReference(self):
        return self.kind in TypeKind.references

    def __repr__(self):
        if self.kind == TypeKind.ARRAY:
            return "{}[]".format(self.context)
        elif self.kind == TypeKind.REF:
            return self.context.name.lexeme
        else:
            return self.kind

    def __eq__(self, other):
        return self.kind == other.kind and self.context == other.context

    def __ne__(self, other):
        return not self.__eq__(other)
