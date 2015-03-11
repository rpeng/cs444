from .common import *
from .interfaces import GetInterfaceMethod
from joos.errors import err
from joos.syntax import *
from structs.utils import memoize


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
def GetImplAndDeclaredSet(node):
    impl = set()
    decl = set()

    if isinstance(node, ClassDecl):
        if node.extends is not None:
            (impl, decl) = GetImplAndDeclaredSet(node.extends.linked_type)

        if node.interfaces is not None:
            for interface in node.interfaces:
                (n_impl, n_decl) = GetImplAndDeclaredSet(interface.linked_type)
                decl |= n_decl

    if isinstance(node, InterfaceDecl):
        if node.extends_interface is not None:
            for interface in node.extends_interface:
                (n_impl, n_decl) = GetImplAndDeclaredSet(interface.linked_type)
                decl |= n_decl

    if node.method_decls is not None:
        for method in node.method_decls:
            modifiers = [x.lexeme for x in method.header.modifiers]
            sig = MakeMethodSig(method.header)
            decl.add(sig)
            if 'abstract' not in modifiers:
                impl.add(sig)
            else:
                if sig in impl:
                    impl.remove(sig)

    return (impl, decl)


def CheckClassMethods(node):
    class_modifiers = [x.lexeme for x in node.modifiers]
    is_abstract = 'abstract' in class_modifiers

    # get method_decls that is not implemented in super interface
    declared = _GetAllDeclaredMethods(node)
    # get implemented methods in current class
    implemented = _GetAllImplementedMethods(node)

    (impl_set, decl_set) = GetImplAndDeclaredSet(node)

    if not is_abstract and (decl_set - impl_set):
        err(node.name, "Abstract method not implemented")

    # Check that all matching sigs have matching types
    all_decls = {}
    for method in declared:
        sig = MakeMethodSig(method.header)
        if sig not in all_decls:
            all_decls[sig] = method
        else:
            other = all_decls[sig]
            if (MakeTypeSig(method.header.m_type) !=
                MakeTypeSig(other.header.m_type)):
                err(node.name,
                    "Type mismatch in method " + method.header.m_id.lexeme)

    if not node.method_decls:
        return

    for decl in node.method_decls:
        modifiers = [x.lexeme for x in decl.header.modifiers]
        if 'abstract' in modifiers and not is_abstract:
            err(decl.header.m_id,
                "Abstract method " + decl.header.m_id.lexeme
                + " in a non abstract class")

        if 'static' not in modifiers:
            sig = tuple(MakeMethodSig(decl.header))
            matched_super_decl = _GetUpstreamMethod(node, sig)
            if matched_super_decl is not None:
                modifiers = [x.lexeme for x in matched_super_decl.header.modifiers]
                if 'static' in modifiers:
                    err(decl.header.m_id,
                        "Non-static method " + decl.header.m_id.lexeme
                        + " replaced a static method")

        sig = tuple(MakeMethodSig(decl.header))
        matched_super_decl = _GetUpstreamMethod(node, sig)
        if matched_super_decl is not None:
            if (MakeTypeSig(decl.header.m_type) !=
                    MakeTypeSig(matched_super_decl.header.m_type)):
                err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                    + " override a method with different return type")

            current_modifiers = [x.lexeme for x in decl.header.modifiers]
            upstream_modifiers = [x.lexeme for x in matched_super_decl.header.modifiers]
            if ('protected' in current_modifiers and
                    'public' in upstream_modifiers):
                err(decl.header.m_id, "Public method " + decl.header.m_id.lexeme
                    + " is replaced with a protected method")

            if ('final' in upstream_modifiers):
                err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                    + " override a final method")

        if node.interfaces is not None:
            for interface in node.interfaces:
                matched_super_decl = GetInterfaceMethod(interface.linked_type, sig)
                if matched_super_decl is not None:
                    if (MakeTypeSig(decl.header.m_type) !=
                    MakeTypeSig(matched_super_decl.header.m_type)):
                        err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                            + " override a method with different return type")

                    current_modifiers = [x.lexeme for x in decl.header.modifiers]
                    if ('protected' in current_modifiers):
                        err(decl.header.m_id, "Public method " +
                            decl.header.m_id.lexeme
                            + " is replaced with a protected method")


@memoize
def _GetAllImplementedMethods(node):
    methods = []
    if node.method_decls is not None:
        for method in node.method_decls:
            modifiers = [x.lexeme for x in method.header.modifiers]
            if 'abstract' not in modifiers:
                methods.append(method)
    if node.extends is not None:
        methods.extend(_GetAllImplementedMethods(node.extends.linked_type))
    else:
        methods.extend(GetObject().method_decls)
    return methods


@memoize
# get method_decls that is not implemented in super interface
def _GetAllDeclaredMethods(node):
    methods = []

    if node.method_decls is not None:
        methods.extend(node.method_decls)

    if isinstance(node, ClassDecl):
        if node.extends is not None:
            methods.extend(_GetAllDeclaredMethods(node.extends.linked_type))
        else:
            methods.extend(GetObject().method_decls)
        if node.interfaces is not None:
            for interface in node.interfaces:
                methods.extend(_GetAllDeclaredMethods(interface.linked_type))
    else:
        if node.extends_interface is not None:
            for interface in node.extends_interface:
                methods.extend(_GetAllDeclaredMethods(interface.linked_type))
        else:
            methods.extend(GetObject().method_decls)
    return methods


@memoize
def _GetUpstreamMethod(node, sig):
    method_decls = None
    if node.extends is not None:
        method_decls = node.extends.linked_type.method_decls
    elif node is not GetObject():
        method_decls = GetObject().method_decls
    if method_decls is not None:
        for decl in method_decls:
            super_sig = tuple(MakeMethodSig(decl.header))
            if sig == super_sig:
                return decl
    if node.extends is not None:
        return _GetUpstreamMethod(node.extends.linked_type, sig)
    return None


def CheckClass(node):
    CheckClassSimple(node)
    CheckClassNoCycles(node)
    CheckDuplicateMethods(node.method_decls)
    CheckConstructors(node.constructor_decls)
    CheckClassMethods(node)
