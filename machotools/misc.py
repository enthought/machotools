# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import macholib.MachO

from macholib import mach_o
from macholib.ptypes import sizeof

from machotools.utils import rstrip_null_bytes, macho_path_as_data, safe_update

def install_name(filename):
    """Returns the install name of a mach-o dylib file."""
    ret = []

    m = macholib.MachO.MachO(filename)
    for header in m.headers:
        install_names = []
        for command in header.commands:
            if command[0].cmd == mach_o.LC_ID_DYLIB:
                install_names.append(rstrip_null_bytes(command[2]))

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

def _create_dylib_command(header, new_install_name, command_index=None):
    if command_index is None:
        command_index = len(header.commands)

    if header.header.magic in (mach_o.MH_MAGIC, mach_o.MH_CIGAM):
        pad_to = 4
    else:
        pad_to = 8
    data = macho_path_as_data(new_install_name, pad_to=pad_to)

    header_size = sizeof(mach_o.load_command) + sizeof(mach_o.dylib_command)
    command_size = header_size + len(data)
    dylib_command = mach_o.dylib_command(header_size, _endian_=header.endian)
    load_command = mach_o.load_command(mach_o.LC_ID_DYLIB, command_size,
                                                _endian_=header.endian)

    header.commands.insert(command_index, (load_command, dylib_command, data))
    header.header.ncmds += 1
    header.changedHeaderSizeBy(command_size)

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
        to_delete = []
        for load_command, dylib_command, data in header.commands:
            if load_command.cmd == mach_o.LC_ID_DYLIB:
                to_delete.append((load_command, dylib_command, data))

        if len(to_delete) < 1:
            raise ValueError("No LC_ID_DYLIB command in {0} ?".format(filename))
        elif len(to_delete) > 1:
            raise ValueError("Unexpected number of LC_ID_DYLIB commands (>1) for {0}".format(filename))
        else:
            to_delete = to_delete[0]

        command_index = _remove_command(header, to_delete)
        _create_dylib_command(header, new_install_name, command_index)

    def writer(f):
        for header in m.headers:
            f.seek(0)
            header.write(f)
    safe_update(filename, writer, "wb")

def dependencies(filename):
    """Returns the list of mach-o the given binary depends on.

    Parameters
    ----------
    filename: str
        Path to the mach-o to query

    Returns
    -------
    dependency_names: seq
        dependency_names[i] is the list of dependencies for the i-th header.
    """
    ret = []

    m = macholib.MachO.MachO(filename)
    for header in m.headers:
        this_ret = []
        for load_command, dylib_command, data in header.commands:
            if load_command.cmd == mach_o.LC_LOAD_DYLIB:
                this_ret.append(rstrip_null_bytes(data))
        ret.append(this_ret)
    return ret
