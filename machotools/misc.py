# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import os
import re
import stat

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
        _change_dylib_command(header, new_install_name)

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

def _change_dylib_command(header, new_install_name):
    command_index, command_tuple = _find_lc_id_dylib(header)
    _change_command_data_inplace(header, command_index, command_tuple, new_install_name)

def _change_dependency_command(header, old_dependency_pattern, new_dependency):
    old_command = _find_specific_lc_load_dylib(header, old_dependency_pattern)
    if old_command is None:
        return
    command_index, command_tuple = old_command
    _change_command_data_inplace(header, command_index, command_tuple, new_dependency)

def _change_command_data_inplace(header, index, old_command, new_data):
    # We change the command 'in-place' to ensure the new dylib command is as
    # close as possible as the old one (same version, timestamp, etc...)
    (old_load_command, old_dylib_command, old_data) = old_command

    if header.header.magic in (mach_o.MH_MAGIC, mach_o.MH_CIGAM):
        pad_to = 4
    else:
        pad_to = 8
    data = macho_path_as_data(new_data, pad_to=pad_to)

    cmdsize_diff = len(data) - len(old_data)
    load_command = old_load_command
    load_command.cmdsize += cmdsize_diff

    dylib_command = old_dylib_command

    header.commands[index] = (load_command, dylib_command, data)
    header.changedHeaderSizeBy(cmdsize_diff)

def _find_lc_dylib_command(header, command_type):
    commands = []
    for command_index, (load_command, dylib_command, data) in enumerate(header.commands):
        if load_command.cmd == command_type:
            commands.append((command_index, (load_command, dylib_command, data)))

    return commands

def _find_lc_id_dylib(header):
    commands = _find_lc_dylib_command(header, mach_o.LC_ID_DYLIB)

    if len(commands) < 1:
        raise ValueError("No LC_ID_DYLIB command in {0} ?".format(filename))
    elif len(commands) > 1:
        raise ValueError("Unexpected number of LC_ID_DYLIB commands (>1) for {0}".format(filename))
    else:
        return commands[0]

def _find_specific_lc_load_dylib(header, dependency_pattern):
    for index, (load_command, dylib_command, data) in \
            _find_lc_dylib_command(header, mach_o.LC_LOAD_DYLIB):
        m = dependency_pattern.search(rstrip_null_bytes(data))
        if m:
            return index, (load_command, dylib_command, data)

def change_dependency(filename, old_dependency_pattern, new_dependency):
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
    _r_old_dependency = re.compile(old_dependency_pattern)
    m = macholib.MachO.MachO(filename)
    for header in m.headers:
        _change_dependency_command(header, _r_old_dependency, new_dependency)

    def writer(f):
        for header in m.headers:
            f.seek(0)
            header.write(f)
    mode = stat.S_IMODE(os.stat(filename).st_mode)
    safe_update(filename, writer, "wb")
    os.chmod(filename, mode)
