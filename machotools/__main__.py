# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import sys

import argparse

from machotools.misc import install_name
from machotools.rpath import list_rpaths_from_file

def list_rpaths_command(namespace):
    rpaths = list_rpaths_from_file(namespace.macho)
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

    namespace = p.parse_args(argv)
    namespace.func(namespace)

if __name__ == "__main__":
    main()
