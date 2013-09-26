from macholib import mach_o

from .utils import macho_path_as_data

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
