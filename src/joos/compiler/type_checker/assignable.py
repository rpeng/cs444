from joos.compiler.type_checker.type_kind import TypeKind
from joos.errors import err

valid_mappings = {
    TypeKind.BOOL: [TypeKind.BOOL],
    TypeKind.BYTE: [TypeKind.BYTE],
    TypeKind.CHAR: [TypeKind.CHAR],
    TypeKind.INT: [TypeKind.BYTE, TypeKind.SHORT, TypeKind.INT, TypeKind.CHAR],
    TypeKind.SHORT: [TypeKind.BYTE, TypeKind.SHORT],
    TypeKind.VOID: [TypeKind.VOID]
}

def CheckAssignable(token, left, right):
    import ipdb; ipdb.set_trace()
    valid = valid_mappings.get(left.kind)
    if valid and right.kind not in valid:
        err(token, "Invalid conversion: {} not assignable to {}".format(
            right.kind, left.kind))
