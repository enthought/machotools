# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import sys

import macholib.MachO

from macholib import mach_o

from .utils import rstrip_null_bytes, safe_update
from .common import _change_command_data_inplace, _find_lc_dylib_command

def install_name(filename):
    """Returns the install name of a mach-o dylib file."""
    m = macholib.MachO.MachO(filename)
    return _install_name_macho(m)

def _install_name_macho(m):
    ret = []

    for header in m.headers:
        install_names = []
        for command in header.commands:
            if command[0].cmd == mach_o.LC_ID_DYLIB:
                data = rstrip_null_bytes(command[2])
                install_name = data.decode(sys.getfilesystemencoding())
                install_names.append(install_name)

        if len(install_names) != 1:
            raise ValueError("Unexpected number of LC_ID_DYLIB commands (%d)" % len(install_names))
        else:
            ret.append(install_names[0])

    return ret

def _remove_command(header, command):
    """Remove the command from the mach-o header.

    command is a 3-tuple with the same format as header.commands"""
    command_index = header.commands.index(command)
    header.commands.remove(command)
    header.header.ncmds -= 1
    header.changedHeaderSizeBy(-command[0].cmdsize)

    return command_index

def change_install_name(filename, new_install_name):
    """Change the install name of a mach-o dylib file.

    For a multi-arch binary, every header is overwritten to the same install
    name

    Parameters
    ----------
    filename: str
        Path to the mach-o file to modify
    new_install_name: str
        New install name
    """
    m = macholib.MachO.MachO(filename)
    for header in m.headers:
        _change_id_dylib_command(header, new_install_name)

    def writer(f):
        for header in m.headers:
            f.seek(0)
            header.write(f)
    safe_update(filename, writer, "wb")

def _change_id_dylib_command(header, new_install_name):
    command_index, command_tuple = _find_lc_id_dylib(header)
    _change_command_data_inplace(header, command_index, command_tuple, new_install_name)

def _find_lc_id_dylib(header):
    commands = _find_lc_dylib_command(header, mach_o.LC_ID_DYLIB)

    filename = header.parent.filename
    if len(commands) < 1:
        raise ValueError("No LC_ID_DYLIB command in {0} ?".format(filename))
    elif len(commands) > 1:
        raise ValueError("Unexpected number of LC_ID_DYLIB commands (>1) for {0}".format(filename))
    else:
        return commands[0]
