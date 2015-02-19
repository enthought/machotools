import os

from macholib.MachO import MachO

def detect_macho_type(path):
    """
    Returns None if not a mach-o.

    Raise an error for non-existing paths.
    """
    if os.stat(path).st_size < 4:
        return None

    try:
        p = MachO(path)
    except ValueError as e:
        # Grrr, why isn't macholib raising proper exceptions...
        assert str(e).startswith("Unknown Mach-O")
        return None
    else:
        if len(p.headers) < 1:
            raise ValueError("No headers in the mach-o file ?")
        else:
            return p.headers[0].filetype

def is_macho(path):
    """Return True if the given path is a Mach-O binary."""
    if os.stat(path).st_size < 4:
        return None

    try:
        MachO(path)
        return True
    except ValueError as e:
        # Grrr, why isn't macholib raising proper exceptions...
        assert str(e).startswith("Unknown Mach-O")
        return False

def is_executable(path):
    """Return True if the given file is a mach-o file of type 'execute'."""
    return detect_macho_type(path) == "execute"

def is_dylib(path):
    """Return True if the given file is a mach-o file of type 'execute'."""
    return detect_macho_type(path) == "dylib"

def is_bundle(path):
    """Return True if the given file is a mach-o file of type 'bundle'."""
    return detect_macho_type(path) == "bundle"
