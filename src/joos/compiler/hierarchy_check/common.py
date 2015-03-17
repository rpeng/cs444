from joos.syntax import *
from joos.errors import err
from structs.utils import memoize

object_sigs = set()
object_decl = None
string_decl = None
cloneable = None
serializable = None

def CheckDuplicateMethods(method_decls):
    if method_decls is None:
        return

    sigs = set()
    for decl in method_decls:
        sig = tuple(MakeMethodSig(decl.header))
        if sig in sigs:
            err(decl.header.m_id,
                "Duplicate method definition: "
                + decl.header.m_id.lexeme)
        sigs.add(sig)


def CheckDuplicateInterfaces(name, nodes):
    decls = set()
    for interface in nodes:
        if interface.linked_type in decls:
            err(name, "Duplicate interface impl: " +
                interface.AsString())
        decls.add(interface.linked_type)


def PopulateObjects(app):
    global object_sigs, object_decl, string_decl, cloneable, serializable
    object_decl = app.type_map.LookupType("java.lang.Object")
    string_decl = app.type_map.LookupType("java.lang.String")
    cloneable = app.type_map.LookupType("java.lang.Cloneable")
    serializable = app.type_map.LookupType("java.io.Serializable")
    if object_decl and object_decl.method_decls:
        for method in object_decl.method_decls:
            object_sigs.add(MakeMethodSig(method.header))


def GetObject():
    return object_decl


def GetStringDecl():
    return string_decl


def GetCloneable():
    return cloneable


def GetSerializable():
    return serializable


@memoize
def MakeTypeSig(type):
    sig = []
    if isinstance(type, ArrayType):
        sig.extend(MakeTypeSig(type.type_or_name))
        sig.append('[]')
    elif isinstance(type, PrimitiveType):
        sig.append(type.t_type.token_type)
    elif isinstance(type, ClassOrInterfaceType):
        sig.append(type.name.linked_type)
    return tuple(sig)


@memoize
def MakeMethodSig(header):
    # Create a signature given a method
    sig = []
    if isinstance(header, MethodHeader):
        sig.append(header.m_id.lexeme)
    # Don't append name for constructors
    if header.params:
        for param in header.params:
            sig.append(MakeTypeSig(param.p_type))
    return tuple(sig)


@memoize
def StrSig(sig):
    result = ""
    if sig:
        if not isinstance(sig[0], tuple):
            result += sig[0]
            result += '(' + ', '.join([str(x[0]) for x in sig[1:]]) + ')'
        else:
            result = '(' + ', '.join([str(x[0]) for x in sig]) + ')'
    return result


@memoize
def LinkInterfaceDecls(node):
    linked = set([node])
    if node.extends_interface:
        for name in node.extends_interface:
            if name.linked_type not in linked:
                linked |= LinkInterfaceDecls(name.linked_type)
    node.linked_interfaces = linked
    return linked
