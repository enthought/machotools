import macholib.MachO

from machotools.definitions import COMMAND_NAME_TO_ID
from machotools.utils import rstrip_null_bytes

def install_name(filename):
    """Returns the install name of a mach-o dylib file."""
    ret = []

    m = macholib.MachO.MachO(filename)
    for header in m.headers:
        install_names = []
        for command in header.commands:
            if command[0].cmd == COMMAND_NAME_TO_ID["LC_ID_DYLIB"]:
                install_names.append(rstrip_null_bytes(command[2]))

        if len(install_names) != 1:
            raise ValueError("Unexpected number of LC_ID_DYLIB commands (%d)" % len(install_names))
        else:
            ret.append(install_names[0])

    return ret
