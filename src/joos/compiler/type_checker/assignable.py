from joos.compiler.type_checker.type_kind import TypeKind
from joos.errors import err
from joos.syntax import ClassDecl, InterfaceDecl

valid_mappings = {
    TypeKind.BOOL: [TypeKind.BOOL],
    TypeKind.BYTE: [TypeKind.BYTE],
    TypeKind.CHAR: [TypeKind.CHAR],
    TypeKind.INT: [TypeKind.BYTE, TypeKind.SHORT, TypeKind.INT, TypeKind.CHAR],
    TypeKind.SHORT: [TypeKind.BYTE, TypeKind.SHORT],
    TypeKind.VOID: [TypeKind.VOID]
}


def _IsClassAssignable(left, right):
    if isinstance(right.context, ClassDecl):
        current = right.context
        while True:
            if current == left.context:
                return True
            if right.context.extends:
                current = right.context.extends.linked_type
            else:
                return False
    else:
        return False


def _IsInterfaceAssignable(left, right):
    seen = set()
    work_list = [right.context]

    while work_list:
        decl = work_list.pop()
        if decl == left.context:
            return True
        seen.add(decl)
        if isinstance(decl, ClassDecl):
            interfaces = decl.interfaces
        elif isinstance(decl, InterfaceDecl):
            interfaces = decl.extends_interface
        else:
            return False
        if interfaces:
            for node in interfaces:
                if node.linked_type not in seen:
                    work_list.append(node.linked_type)
    return False


def IsAssignable(left, right):
    if isinstance(left, str):
        left = TypeKind(left)
    if isinstance(right, str):
        right = TypeKind(right)

    valid = valid_mappings.get(left.kind)

    if valid and right.kind not in valid:
        return False

    if left.kind == TypeKind.ARRAY and left != right:
        return False

    if left.kind == TypeKind.REF:
        if right.kind == TypeKind.NULL:
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
        err(token, "Invalid conversion: {} not comparable to {}".format(
            right, left))

