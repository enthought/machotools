import macholib.MachO
import macholib.mach_o

from macholib.ptypes import sizeof

from machotools.utils import rstrip_null_bytes, macho_path_as_data

def list_rpaths_from_file(filename):
    """Get the list of rpaths defined in the given mach-o binary.

    The returned value is a list rpaths such as rpaths[i] is the list of rpath
    in the i-th header.

    Note
    ----
    The '\0' padding at the end of each rpath is stripped

    Parameters
    ----------
    filename: str
        The path to the mach-o binary file to look at
    """
    rpaths = []

    m = macholib.MachO.MachO(filename)
    for header in m.headers:
        header_rpaths = []
        rpath_commands = [command for command in header.commands if
                isinstance(command[1], macholib.mach_o.rpath_command)]
        for rpath_command in rpath_commands:
            rpath = rpath_command[2]
            if not rpath.endswith("\x00"):
                raise ValueError("Unexpected end character for rpath command value: %r".format(rpath))
            else:
                header_rpaths.append(rstrip_null_bytes(rpath))
        rpaths.append(header_rpaths)

    return rpaths

def add_rpaths_to_file(filename, rpaths):
    """Add the given list of path rpaths to all header in a MachO file.

    Parameters
    ----------
    filename: str
        The path to the macho-o binary file to add rpath to
    rpaths: seq
        List of paths to add as rpath to the mach-o binary
    """
    macho = macholib.MachO.MachO(filename)
    for header in macho.headers:
        for rpath in rpaths:
            _add_rpath_to_header(header, rpath)

    with open(filename, 'rb+') as f:
        for header in macho.headers:
            f.seek(0)
            header.write(f)

def _add_rpath_to_header(header, rpath):
    """Add an LC_RPATH load command to a MachOHeader.

    Parameters
    ----------
    header: MachOHeader instances
        A mach-o header to add rpath to
    rpath: str
        The rpath to add to the given header
    """
    if header.header.magic in (macholib.mach_o.MH_MAGIC, macholib.mach_o.MH_CIGAM):
        pad_to = 4
    else:
        pad_to = 8
    data = macho_path_as_data(rpath, pad_to=pad_to)
    header_size = sizeof(macholib.mach_o.load_command) + sizeof(macholib.mach_o.rpath_command)
    command_size = header_size + len(data)
    cmd = macholib.mach_o.rpath_command(header_size, _endian_=header.endian)
    lc = macholib.mach_o.load_command(macholib.mach_o.LC_RPATH, command_size,
        _endian_=header.endian)
    header.commands.append((lc, cmd, data))
    header.header.ncmds += 1
    header.changedHeaderSizeBy(command_size)
