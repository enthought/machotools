# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import sys

import argparse

from machotools import change_install_name, install_name, change_dependency, dependencies
from machotools.rpath import list_rpaths

def list_rpaths_command(namespace):
    rpaths = list_rpaths(namespace.macho)
    if not len(rpaths) == 1:
        raise ValueError("Multi-arch files not supported yet !")
    else:
        for rpath in rpaths[0]:
            print rpath

def list_install_names(namespace):
    install_names = install_name(namespace.macho)
    if not len(install_names) == 1:
        raise ValueError("Multi-arch files not supported yet !")
    else:
        for name in install_names:
            print name

def change_install_name_command(namespace):
    change_install_name(namespace.macho, namespace.install_name)

def change_dependency_name_command(namespace):
    change_dependency(namespace.macho, namespace.old_library_pattern, namespace.new_library)

def list_dependency_name_command(namespace):
    deps = dependencies(namespace.macho)
    if not len(deps) == 1:
        raise ValueError("Multi-arch files not supported yet !")
    else:
        for dep in deps[0]:
            print dep

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    p = argparse.ArgumentParser()
    sub_parsers = p.add_subparsers(title="sub commands")

    rpath = sub_parsers.add_parser("list_rpaths", help="Manipulate rpaths")
    rpath.add_argument("macho", help="Path to the mach-o to manipulate")
    rpath.set_defaults(func=list_rpaths_command)

    install_name_parser = sub_parsers.add_parser("install_name", help="Manipulate rpaths")
    install_name_parser.add_argument("macho", help="Path to the mach-o to manipulate")
    install_name_parser.set_defaults(func=list_install_names)

    change_install_name_parser = sub_parsers.add_parser("change_install_name", help="Change install_name")
    change_install_name_parser.add_argument("macho", help="Path to the mach-o to manipulate")
    change_install_name_parser.add_argument("install_name", help="New install name")
    change_install_name_parser.set_defaults(func=change_install_name_command)

    change_dependency_name_parser = sub_parsers.add_parser("change_library",
            help="Change library dependency")
    change_dependency_name_parser.add_argument("macho", help="Path to the mach-o to manipulate")
    change_dependency_name_parser.add_argument("old_library_pattern", help="Old library to change (can be a regex)")
    change_dependency_name_parser.add_argument("new_library",
            help="New library to replace the old one with") 
    change_dependency_name_parser.set_defaults(func=change_dependency_name_command)

    list_dependency_name_parser = sub_parsers.add_parser("list_libraries",
            help="Change library dependency")
    list_dependency_name_parser.add_argument("macho", help="Path to the mach-o to manipulate")
    list_dependency_name_parser.set_defaults(func=list_dependency_name_command)

    namespace = p.parse_args(argv)
    namespace.func(namespace)

if __name__ == "__main__":
    main()
