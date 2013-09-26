# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import sys

import argparse

from .macho_rewriter import rewriter_factory

def list_rpaths_command(namespace):
    rewriter = rewriter_factory(namespace.macho)
    for rpath in rewriter.rpaths:
        print(rpath)

def list_install_names(namespace):
    rewriter = rewriter_factory(namespace.macho)
    print(rewriter.install_name)

def change_install_name_command(namespace):
    with rewriter_factory(namespace.macho) as rewriter:
        rewriter.install_name = namespace.install_name

def change_dependency_name_command(namespace):
    with rewriter_factory(namespace.macho) as rewriter:
        rewriter.change_dependency(namespace.old_library_pattern,
                                   namespace.new_library)

def list_dependency_name_command(namespace):
    rewriter = rewriter_factory(namespace.macho)
    for dependency in rewriter.dependencies:
        print(dependency)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    p = argparse.ArgumentParser()
    sub_parsers = p.add_subparsers(title="sub commands")

    rpath = sub_parsers.add_parser("list_rpaths", help="Print rpaths")
    rpath.add_argument("macho", help="Path to the mach-o to manipulate")
    rpath.set_defaults(func=list_rpaths_command)

    install_name_parser = sub_parsers.add_parser("install_name", help="Print the install name")
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
