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

    if node.method_decls is not None:
        for decl in node.method_decls:
            sig = tuple(MakeMethodSig(decl.header))
            matched_super_decl = GetUpstreamInterfaceMethod(node, sig)
            if matched_super_decl is not None:
                if (MakeTypeSig(decl.header.m_type) !=
                    MakeTypeSig(matched_super_decl.header.m_type)):
                        err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                            + " override a method with different return type")

                upstream_modifiers = [x.lexeme for x in matched_super_decl.header.modifiers]
                if ('final' in upstream_modifiers):
                    err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                        + " override a final method")


@memoize
def GetUpstreamInterfaceMethod(node, sig):
    if node.extends_interface:
        for iface in node.extends_interface:
            decl = GetInterfaceMethod(iface.linked_type, sig)
            if decl is not None:
                return decl
    else:
        return GetInterfaceMethod(GetObject(), sig)


@memoize
def GetInterfaceMethod(node, sig):
    method_decls = node.method_decls
    if method_decls is not None:
        for decl in method_decls:
            obj_sig = tuple(MakeMethodSig(decl.header))
            if obj_sig == sig:
                return decl

    if isinstance(node, InterfaceDecl):
        if node.extends_interface:
            for interface in node.extends_interface:
                method = GetInterfaceMethod(interface.linked_type, sig)
                if method is not None:
                    return method
        else:
            return GetInterfaceMethod(GetObject(), sig)
    return None

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



def CheckInterface(node):
    CheckInterfaceSimple(node)
    CheckInterfaceNoCycles(node)
    CheckDuplicateMethods(node.method_decls)
