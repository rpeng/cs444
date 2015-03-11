from .common import *
from joos.compiler.hierarchy_check.interfaces import ResolveInterfaceDecls, AddDecls
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


def CheckConstructors(constructor_decls):
    if constructor_decls is None:
        return

    sigs = set()
    for decl in constructor_decls:
        sig = tuple(MakeMethodSig(decl))
        if sig in sigs:
            err(decl.name,
                "Duplicate constructor definition: "
                + decl.name.lexeme)
        sigs.add(sig)


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
def ResolveClassMethods(node):
    # Returns decls: set(MethodDecls)
    decl_map = {}

    if node.interfaces:
        for interface in node.interfaces:
            decls = ResolveInterfaceDecls(interface.linked_type)
            AddDecls(decls, decl_map)

    if node.extends:
        decls = ResolveClassMethods(node.extends.linked_type)
        AddDecls(decls, decl_map)
    else:
        AddDecls(GetObject().method_decls, decl_map)

    AddDecls(node.method_decls, decl_map)

    class_modifiers = [x.lexeme for x in node.modifiers]
    if 'abstract' not in class_modifiers:
        for decl in decl_map.values():
            if decl.IsAbstract():
                err(node.name,
                    "Non abstract class must implement all methods: " + decl.header.m_id)

    return set(decl_map.values())


def CheckClass(node):
    CheckClassSimple(node)
    CheckClassNoCycles(node)
    CheckConstructors(node.constructor_decls)
    CheckDuplicateMethods(node.method_decls)
    ResolveClassMethods(node)

