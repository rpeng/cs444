import collections
from .common import *
from .interfaces import ResolveLinkInterfaceDecls, AddDecls
from joos.errors import err
from joos.syntax import *


acyclic_class_nodes = set()


def CheckClassNoCycles(node):
    if node in acyclic_class_nodes:
        return

    visited_set = set(node)
    while True:
        extends = node.extends
        if extends:
            node = extends.linked_type
            if node in visited_set:
                err(node.name, "Cyclic inheritance of: " + extends.AsString())
            visited_set.add(node)
        else:
            break

    acyclic_class_nodes.add(node)


def CheckLinkConstructors(node):
    if node.constructor_decls is None:
        return

    cons_map = {}
    for decl in node.constructor_decls:
        sig = tuple(MakeMethodSig(decl))
        if sig in cons_map:
            err(decl.name,
                "Duplicate constructor definition: "
                + decl.name.lexeme)
        cons_map[sig] = decl

    node.cons_map = cons_map


def CheckClassSimple(node):
    class_modifiers = [x.lexeme for x in node.modifiers]
    is_abstract = 'abstract' in class_modifiers

    if node.extends is not None:
        if not isinstance(
                node.extends.linked_type, ClassDecl):
            err(node.name, "A class must extend a class")
        else:
            modifiers = [x.lexeme for x in node.extends.linked_type.modifiers]
            if 'final' in modifiers:
                err(node.name, "A class must not extend a final class")

    if node.interfaces is not None:
        CheckDuplicateInterfaces(node.name, node.interfaces)
        for interface in node.interfaces:
            if not isinstance(interface.linked_type, InterfaceDecl):
                err(node.name, "A class must implement an interface.")


@memoize
def ResolveLinkClassMethods(node):
    # Returns decls: set(MethodDecls)
    decl_map = collections.OrderedDict()
    class_modifiers = [x.lexeme for x in node.modifiers]
    is_abstract = 'abstract' in class_modifiers

    if node.interfaces:
        for interface in node.interfaces:
            decls = ResolveLinkInterfaceDecls(interface.linked_type)
            AddDecls(decls, decl_map)

    if node.extends:
        decls = ResolveLinkClassMethods(node.extends.linked_type)
        AddDecls(decls, decl_map, is_abstract)
    elif GetObject():
        AddDecls(GetObject().method_decls, decl_map, is_abstract)

    if node is not GetObject():
        AddDecls(node.method_decls, decl_map, is_abstract)

    if not is_abstract:
        for decl in decl_map.values():
            if decl.IsAbstract():
                err(node.name,
                    "Non abstract class must implement all methods: " +
                    decl.header.m_id.lexeme)

    node.method_map = decl_map
    return set(decl_map.values())


def GetAndLinkOrderedFields(node):
    if node.ordered_fields is not None:
        return node.ordered_fields
    fields = []
    if node.extends:
        fields.extend(GetAndLinkOrderedFields(node.extends.linked_type))
    if node.field_decls:
        for field in node.field_decls:
            if not field.IsStatic():
                fields.append(field)
    node.ordered_fields = fields
    return fields


def LinkClass(node):
    ifaces = set()
    if node.interfaces:
        for name in node.interfaces:
            ifaces |= LinkInterfaceDecls(name.linked_type)
    node.linked_interfaces = ifaces

    supers = [node]
    current = node.extends and node.extends.linked_type
    while current:
        supers.append(current)
        current = current.extends and current.extends.linked_type
    node.linked_supers = supers
    GetAndLinkOrderedFields(node)


def CheckClass(node):
    CheckClassSimple(node)
    CheckClassNoCycles(node)
    CheckLinkConstructors(node)
    CheckDuplicateMethods(node.method_decls)
    ResolveLinkClassMethods(node)
    LinkClass(node)
