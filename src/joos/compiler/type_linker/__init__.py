from joos.compiler.type_linker.type_map import TypeMap
from type_linker import TypeLinker


__all__ = ['LinkTypes']


def LinkTypes(list_of_nodes):
    map = TypeMap()
    for node in list_of_nodes:
        map.AddNode(node)
    linker = TypeLinker(map)
    for node in list_of_nodes:
        node.visit(linker)
