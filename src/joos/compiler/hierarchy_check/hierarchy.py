from joos.errors import err
from joos.syntax import *
from structs.utils import memoize


acyclic_class_nodes = set()
acyclic_interface_nodes = set()


def _CheckInterfaces(name, nodes):
    decls = set()
    for interface in nodes:
        if interface.linked_type in decls:
            err(name, "Duplicate interface impl: " +
                interface.AsString())
        decls.add(interface.linked_type)


def _CheckInterfaceSimple(node):
    if node.extends_interface:
        _CheckInterfaces(node.name, node.extends_interface)
        for interface in node.extends_interface:
            if not isinstance(interface.linked_type, InterfaceDecl):
                err(node.name, "An interface must not extend a class: " +
                    interface.AsString())


def _CheckClassSimple(node):
    class_modifiers = [x.lexeme for x in node.modifiers]
    isAbstract = 'abstract' in class_modifiers

    if node.extends is not None:
        if not isinstance(
                node.extends.linked_type, ClassDecl):
            err(node.name, "A class must extend a class")
        else:
            modifiers = [x.lexeme for x in node.extends.linked_type.modifiers]
            if 'final' in modifiers:
                err(node.name, "A class must not extend a final class")

        # get method_decls that is not implemented in super class
        super_methods = node.extends.linked_type.method_decls
        super_abstract_methods = []
        if super_methods is not None:
            for decl in super_methods:
                modifiers = [x.lexeme for x in decl.header.modifiers]
                if 'abstract' in modifiers:
                    sig = tuple(_MakeMethodSig(decl.header))
                    super_abstract_methods.append(sig)
        # get implemented methods in current class
        current_implemented_methods = []
        if node.method_decls is not None:
            for decl in node.method_decls:
                if decl.body_block is not None:
                    sig = tuple(_MakeMethodSig(decl.header))
                    current_implemented_methods.append(sig)
        # check if super_abstract_methods are implemented in current class
        for sig in super_abstract_methods:
            if sig not in current_implemented_methods and not isAbstract:
                err(node.name,
                    "Inherited abstract method not implemented")

    if node.interfaces is not None:
        _CheckInterfaces(node.name, node.interfaces)
        for interface in node.interfaces:
            if not isinstance(interface.linked_type, InterfaceDecl):
                err(node.name, "A class must implement an interface.")

        # get method_decls that is not implemented in super interface
        super_abstract_methods = set()
        for interface in node.interfaces:
            super_abstract_methods |= _GetMethodDeclsFromInterfaces(
                interface.linked_type)
        # get implemented methods in current class
        current_implemented_methods = []
        if node.method_decls is not None:
            for decl in node.method_decls:
                sig = tuple(_MakeMethodSig(decl.header))
                current_implemented_methods.append(sig)
        # check if super_abstract_methods are implemented in current class
        for sig in super_abstract_methods:
            if sig not in current_implemented_methods and not isAbstract:
                err(node.name,
                    "Inherited interface method not declared or implemented")


@memoize
# get method_decls that is not implemented in super interface
def _GetMethodDeclsFromInterfaces(node):
    super_abstract_methods = set()

    if node.extends_interface is not None:
        for interface in node.extends_interface:
            super_methods = interface.linked_type.method_decls
            if super_methods is not None:
                for decl in super_methods:
                    sig = tuple(_MakeMethodSig(decl.header))
                    super_abstract_methods.add(sig)
            super_abstract_methods |= _GetMethodDeclsFromInterfaces(
                interface.linked_type)

    return super_abstract_methods


def _CheckClassNoCycles(node):
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


def _CheckInterfaceNoCycles(node, path=None):
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
            _CheckInterfaceNoCycles(name.linked_type, path)
        path.remove(node)
    acyclic_interface_nodes.add(node)


def _MakeTypeSig(type):
    sig = []
    if isinstance(type, ArrayType):
        sig.extend(_MakeTypeSig(type.type_or_name))
        sig.append('[]')
    elif isinstance(type, PrimitiveType):
        sig.append(type.t_type.token_type)
    elif isinstance(type, ClassOrInterfaceType):
        sig.append(type.name.linked_type)
    return tuple(sig)


def _MakeMethodSig(header):
    # Create a signature given a method
    sig = []
    if isinstance(header, MethodHeader):
        sig.append(header.m_id.lexeme)
    elif isinstance(header, ConstructorDecl):
        sig.append(header.name.lexeme)
    if header.params:
        for param in header.params:
            sig.append(_MakeTypeSig(param.p_type))
    return tuple(sig)


def _CheckMethods(method_decls):
    if method_decls is None:
        return

    sigs = set()
    for decl in method_decls:
        sig = tuple(_MakeMethodSig(decl.header))
        if sig in sigs:
            err(decl.header.m_id,
                "Duplicate method definition: "
                + decl.header.m_id.lexeme)
        sigs.add(sig)


def _CheckConstructors(constructor_decls):
    if constructor_decls is None:
        return

    sigs = set()
    for decl in constructor_decls:
        sig = tuple(_MakeMethodSig(decl))
        if sig in sigs:
            err(decl.name,
                "Duplicate constructor definition: "
                + decl.name.lexeme)
        sigs.add(sig)


def _CheckClassMethods(node, method_decls):
    if method_decls is None:
        return

    class_modifiers = [x.lexeme for x in node.modifiers]
    isAbstract = 'abstract' in class_modifiers

    for decl in method_decls:
        modifiers = [x.lexeme for x in decl.header.modifiers]
        if 'abstract' in modifiers and not isAbstract:
            err(decl.header.m_id,
                "Abstract method " + decl.header.m_id.lexeme
                + " in a non abstract class")


def _CheckClass(node):
    _CheckClassSimple(node)
    _CheckClassNoCycles(node)
    _CheckMethods(node.method_decls)
    _CheckConstructors(node.constructor_decls)
    _CheckClassMethods(node, node.method_decls)


def _CheckInterface(node):
    _CheckInterfaceSimple(node)
    _CheckInterfaceNoCycles(node)
    _CheckMethods(node.method_decls)


def _CheckNode(node):
    if node.type_decl:
        if isinstance(node.type_decl, ClassDecl):
            _CheckClass(node.type_decl)
        else:
            _CheckInterface(node.type_decl)


def CheckHierarchy(ast_nodes):
    for node in ast_nodes:
        _CheckNode(node)
