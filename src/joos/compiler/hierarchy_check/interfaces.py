from .common import *
from joos.errors import err
from joos.syntax import *


acyclic_interface_nodes = set()


def CheckInterfaceSimple(node):
    if node.extends_interface:
        CheckDuplicateInterfaces(node.name, node.extends_interface)
        for interface in node.extends_interface:
            if not isinstance(interface.linked_type, InterfaceDecl):
                err(node.name, "An interface must not extend a class: " +
                    interface.AsString())


def CheckInterfaceNoCycles(node, path=None):
    if node in acyclic_interface_nodes:
        return

    if path is None:
        path = set()

    if node.extends_interface:
        path.add(node)
        for name in node.extends_interface:
            if name.linked_type in path:
                err(node.name,
                    "Cyclic interface extends: " + name.AsString())
            CheckInterfaceNoCycles(name.linked_type, path)
        path.remove(node)
    acyclic_interface_nodes.add(node)


def AddDecls(new_decls, decls_map):
    if new_decls is None:
        return

    for decl in new_decls:
        sig = MakeMethodSig(decl.header)
        if sig in decls_map and decls_map[sig] != decl:
            VerifyReplaceDecl(decls_map[sig], decl)
        decls_map[sig] = decl


def VerifyReplaceDecl(old_decl, new_decl):
    old_header = old_decl.header
    new_header = new_decl.header

    old_modifiers = [x.lexeme for x in old_header.modifiers]
    new_modifiers = [x.lexeme for x in new_header.modifiers]

    m_name = new_header.m_id.lexeme

    # Check return types match
    if MakeTypeSig(old_header.m_type) != MakeTypeSig(new_header.m_type):
        err(new_header.m_id, "Return type mismatch in: " + m_name)

    # Check static -> non_static
    if 'static' in old_modifiers and 'static' not in new_modifiers:
        err(new_header.m_id, "Static replaced with non-static in: " + m_name)

    # Check nonstatic -> static
    if 'static' not in old_modifiers and 'static' in new_modifiers:
        err(new_header.m_id, "Non-static replaced with static in: " + m_name)

    # Check public -> protected
    if 'public' in old_modifiers and 'protected' in new_modifiers:
        err(new_header.m_id, "Public replaced with protected in: " + m_name)

    # Check override final
    if 'final' in old_modifiers:
        err(new_header.m_id, "Attempt to override final method: " + m_name)


@memoize
def ResolveInterfaceDecls(node):
    decls_map = {}
    if node.extends_interface:
        for name in node.extends_interface:
            new_decls = ResolveInterfaceDecls(name.linked_type)
            AddDecls(new_decls, decls_map)
    else:
        AddDecls(GetObject().method_decls, decls_map)
    AddDecls(node.method_decls, decls_map)
    return set(decls_map.values())


def CheckInterface(node):
    CheckInterfaceSimple(node)
    CheckInterfaceNoCycles(node)
    CheckDuplicateMethods(node.method_decls)
    ResolveInterfaceDecls(node)
