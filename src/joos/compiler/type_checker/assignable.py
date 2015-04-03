from joos.compiler.hierarchy_check.common import GetObject, GetCloneable, GetSerializable
from joos.compiler.type_checker.type_kind import TypeKind
from joos.errors import err
from joos.syntax import ClassDecl, InterfaceDecl

valid_mappings = {
    TypeKind.BOOL: [TypeKind.BOOL],
    TypeKind.INT: [TypeKind.BYTE, TypeKind.SHORT, TypeKind.INT, TypeKind.CHAR],
    TypeKind.CHAR: [TypeKind.CHAR],
    TypeKind.BYTE: [TypeKind.BYTE],
    TypeKind.SHORT: [TypeKind.BYTE, TypeKind.SHORT],
    TypeKind.VOID: [TypeKind.VOID]
}


def _IsClassAssignable(left, right):
    if not isinstance(right.context, ClassDecl):
        return False
    return left.context in right.context.linked_supers


def _IsInterfaceAssignable(left, right):
    if (isinstance(right.context, ClassDecl)
        or isinstance(right.context, InterfaceDecl)):
        return left.context in right.context.linked_interfaces
    elif right.kind == TypeKind.ARRAY:
        return left.context in [GetCloneable(), GetSerializable()]
    return False


def _ToInstance(left, right):
    if isinstance(left, str):
        left = TypeKind(left)
    if isinstance(right, str):
        right = TypeKind(right)
    return (left, right)


def CanAssign(left, right):
    left, right = _ToInstance(left, right)

    if left.kind in TypeKind.primitives and right.kind in TypeKind.primitives:
        valid = valid_mappings.get(left.kind)
        return right.kind in valid

    if left.kind == TypeKind.ARRAY:
        if right.kind == TypeKind.NULL:
            return True
        if right.kind == TypeKind.ARRAY:
            if left.context.kind in TypeKind.primitives:
                return left.context.kind == right.context.kind
            return CanAssign(left.context, right.context)
        else:
            return False

    if left.kind == TypeKind.REF or left.kind == TypeKind.CLASS:
        if right.kind == TypeKind.NULL:
            return True
        if left.context == GetObject() and right.kind in TypeKind.references:
            return True
        if isinstance(left.context, ClassDecl):
            return _IsClassAssignable(left, right)
        elif isinstance(left.context, InterfaceDecl):
            return _IsInterfaceAssignable(left, right)

    return left.kind == right.kind


def CanCompare(left, right):
    return CanAssign(left, right) or CanAssign(right, left)


def CheckAssignable(token, left, right):
    if not CanAssign(left, right):
        err(token, "Cannot assign {} to {}".format(right, left))


def CheckCanConvert(token, left, right):
    if not CanAssign(left, right):
        err(token, "Invalid conversion: got {} expected {}".format(
            right, left))


def CheckCastable(token, left, right):
    left, right = _ToInstance(left, right)
    if left.kind in TypeKind.numerics and right.kind in TypeKind.numerics:
        return
    if not CanCompare(left, right):
        err(token, "Cannot cast {} to {}".format(right, left))


def CheckComparable(token, left, right):
    if not CanCompare(left, right):
        err(token, "Invalid conversion: cannot interchange {} and {}".format(
            right, left))

