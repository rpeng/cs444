from joos.compiler.hierarchy_check.common import GetObject, GetCloneable, GetSerializable
from joos.compiler.type_checker.type_kind import TypeKind
from joos.errors import err
from joos.syntax import ClassDecl, InterfaceDecl

valid_mappings = {
    TypeKind.BOOL: [TypeKind.BOOL],
    TypeKind.BYTE: [TypeKind.BYTE, TypeKind.CHAR],
    TypeKind.CHAR: [TypeKind.CHAR, TypeKind.BYTE],
    TypeKind.INT: [TypeKind.BYTE, TypeKind.SHORT, TypeKind.INT, TypeKind.CHAR],
    TypeKind.SHORT: [TypeKind.BYTE, TypeKind.SHORT, TypeKind.CHAR],
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


def IsAssignable(left, right):
    if isinstance(left, str):
        left = TypeKind(left)
    if isinstance(right, str):
        right = TypeKind(right)

    valid = valid_mappings.get(left.kind)

    if valid:
        return right.kind in valid

    if left.kind == TypeKind.ARRAY:
        if right.kind == TypeKind.NULL:
            return True
        if right.kind == TypeKind.ARRAY:
            return IsAssignable(left.context, right.context)
        else:
            return False

    if left.kind == TypeKind.REF:
        if right.kind == TypeKind.NULL:
            return True
        if left.context == GetObject() and right.kind in TypeKind.references:
            return True
        if isinstance(left.context, ClassDecl):
            return _IsClassAssignable(left, right)
        elif isinstance(left.context, InterfaceDecl):
            return _IsInterfaceAssignable(left, right)

    return left.kind == right.kind


def CheckAssignable(token, left, right):
    if not IsAssignable(left, right):
        err(token, "Invalid conversion: got {} expected {}".format(
            right, left))


def CheckComparable(token, left, right):
    if not (IsAssignable(left, right) or IsAssignable(right, left)):
        err(token, "Invalid conversion: cannot interchange {} and {}".format(
            right, left))

