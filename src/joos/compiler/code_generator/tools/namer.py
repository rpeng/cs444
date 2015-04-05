def ClassOrInterfaceName(class_or_interface_decl):
    pkg = class_or_interface_decl.env.LookupPackage()
    name = class_or_interface_decl.name.lexeme

    if pkg:
        return "{}.{}".format(pkg[0], name)
    else:
        return name
