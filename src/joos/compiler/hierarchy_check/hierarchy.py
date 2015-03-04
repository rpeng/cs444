from joos.errors import err
from joos.syntax import *
from structs.utils import memoize


acyclic_class_nodes = set()
acyclic_interface_nodes = set()
object_sigs = set()
object_decl = None


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

    if node.method_decls is not None:
        for decl in node.method_decls:
            sig = tuple(_MakeMethodSig(decl.header))
            matched_super_decl = _GetUpstreamInterfaceMethod(node, sig)
            if matched_super_decl is not None:
                if (_MakeTypeSig(decl.header.m_type) !=
                    _MakeTypeSig(matched_super_decl.header.m_type)):
                        err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                            + " override a method with different return type")

                upstream_modifiers = [x.lexeme for x in matched_super_decl.header.modifiers]
                if ('final' in upstream_modifiers):
                    err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                        + " override a final method")


@memoize
def _GetUpstreamInterfaceMethod(node, sig):
    if node.extends_interface:
        for iface in node.extends_interface:
            decl = _GetInterfaceMethod(iface.linked_type, sig)
            if decl is not None:
                return decl
    else:
        return _GetInterfaceMethod(object_decl, sig)


@memoize
def _GetInterfaceMethod(node, sig):
    method_decls = node.method_decls
    if method_decls is not None:
        for decl in method_decls:
            obj_sig = tuple(_MakeMethodSig(decl.header))
            if obj_sig == sig:
                return decl

    if isinstance(node, InterfaceDecl):
        if node.extends_interface:
            for interface in node.extends_interface:
                method = _GetInterfaceMethod(interface.linked_type, sig)
                if method is not None:
                    return method
        else:
            return _GetInterfaceMethod(object_decl, sig)
    return None


def _CheckClassSimple(node):
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
        _CheckInterfaces(node.name, node.interfaces)
        for interface in node.interfaces:
            if not isinstance(interface.linked_type, InterfaceDecl):
                err(node.name, "A class must implement an interface.")


@memoize
def _GetImplAndDeclaredSet(node):
    impl = set()
    decl = set()

    if isinstance(node, ClassDecl):
        if node.extends is not None:
            (impl, decl) = _GetImplAndDeclaredSet(node.extends.linked_type)

        if node.interfaces is not None:
            for interface in node.interfaces:
                (n_impl, n_decl) = _GetImplAndDeclaredSet(interface.linked_type)
                decl |= n_decl

    if isinstance(node, InterfaceDecl):
        if node.extends_interface is not None:
            for interface in node.extends_interface:
                (n_impl, n_decl) = _GetImplAndDeclaredSet(interface.linked_type)
                decl |= n_decl

    if node.method_decls is not None:
        for method in node.method_decls:
            modifiers = [x.lexeme for x in method.header.modifiers]
            sig = _MakeMethodSig(method.header)
            decl.add(sig)
            if 'abstract' not in modifiers:
                impl.add(sig)
            else:
                if sig in impl:
                    impl.remove(sig)

    return (impl, decl)


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
        methods.extend(object_decl.method_decls)
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
            methods.extend(object_decl.method_decls)
        if node.interfaces is not None:
            for interface in node.interfaces:
                methods.extend(_GetAllDeclaredMethods(interface.linked_type))
    else:
        if node.extends_interface is not None:
            for interface in node.extends_interface:
                methods.extend(_GetAllDeclaredMethods(interface.linked_type))
        else:
            methods.extend(object_decl.method_decls)
    return methods


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


@memoize
def _MakeTypeSig(type):
    sig = []
    if isinstance(type, ArrayType):
        sig.extend(_MakeTypeSig(type.type_or_name))
        sig.append('[]')
    elif isinstance(type, PrimitiveType):
        sig.append(type.t_type.token_type)
    elif isinstance(type, ClassOrInterfaceType):
        sig.append(type.name.linked_type)
    elif isinstance(type, VoidType):
        sig.append('void')
    return tuple(sig)


@memoize
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


def _CheckClassMethods(node):
    class_modifiers = [x.lexeme for x in node.modifiers]
    is_abstract = 'abstract' in class_modifiers

    # get method_decls that is not implemented in super interface
    declared = _GetAllDeclaredMethods(node)
    # get implemented methods in current class
    implemented = _GetAllImplementedMethods(node)

    (impl_set, decl_set) = _GetImplAndDeclaredSet(node)

    if not is_abstract and (decl_set - impl_set):
        err(node.name, "Abstract method not implemented")

    # Check that all matching sigs have matching types
    all_decls = {}
    for method in declared:
        sig = _MakeMethodSig(method.header)
        if sig not in all_decls:
            all_decls[sig] = method
        else:
            other = all_decls[sig]
            if (_MakeTypeSig(method.header.m_type) !=
                _MakeTypeSig(other.header.m_type)):
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
            sig = tuple(_MakeMethodSig(decl.header))
            matched_super_decl = _GetUpstreamMethod(node, sig)
            if matched_super_decl is not None:
                modifiers = [x.lexeme for x in matched_super_decl.header.modifiers]
                if 'static' in modifiers:
                    err(decl.header.m_id,
                        "Non-static method " + decl.header.m_id.lexeme
                        + " replaced a static method")

        sig = tuple(_MakeMethodSig(decl.header))
        matched_super_decl = _GetUpstreamMethod(node, sig)
        if matched_super_decl is not None:
            if (_MakeTypeSig(decl.header.m_type) !=
                    _MakeTypeSig(matched_super_decl.header.m_type)):
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
                matched_super_decl = _GetInterfaceMethod(interface.linked_type, sig)
                if matched_super_decl is not None:
                    if (_MakeTypeSig(decl.header.m_type) !=
                    _MakeTypeSig(matched_super_decl.header.m_type)):
                        err(decl.header.m_id, "Method " + decl.header.m_id.lexeme
                            + " override a method with different return type")

                    current_modifiers = [x.lexeme for x in decl.header.modifiers]
                    if ('protected' in current_modifiers):
                        err(decl.header.m_id, "Public method " +
                            decl.header.m_id.lexeme
                            + " is replaced with a protected method")


@memoize
def _GetUpstreamMethod(node, sig):
    method_decls = None
    if node.extends is not None:
        method_decls = node.extends.linked_type.method_decls
    elif node is not object_decl:
        method_decls = object_decl.method_decls
    if method_decls is not None:
        for decl in method_decls:
            super_sig = tuple(_MakeMethodSig(decl.header))
            if sig == super_sig:
                return decl
    if node.extends is not None:
        return _GetUpstreamMethod(node.extends.linked_type, sig)
    return None


def _CheckClass(node):
    _CheckClassSimple(node)
    _CheckClassNoCycles(node)
    _CheckMethods(node.method_decls)
    _CheckConstructors(node.constructor_decls)
    _CheckClassMethods(node)


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


def _PopulateObject(app):
    global object_sigs, object_decl
    object_decl = app.type_map.LookupType("java.lang.Object")
    if object_decl.method_decls:
        for method in object_decl.method_decls:
            object_sigs.add(_MakeMethodSig(method.header))


def CheckHierarchy(app):
    _PopulateObject(app)
    for node in app.compilation_units:
        _CheckNode(node)
