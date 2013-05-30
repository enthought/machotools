from macholib.MachO import MachO

def _is_macho_type(path, macho_type):
    try:
        p = MachO(path)
    except ValueError as e:
        # Grrr, why isn't macholib raising proper exceptions...
        assert str(e).startswith("Unknown Mach-O")
        return False
    else:
        if len(p.headers) < 1:
            raise ValueError("No headers in the mach-o file ?")
        else:
            return p.headers[0].filetype == macho_type

def is_macho(path):
    """Return True if the given path is a Mach-O binary."""
    try:
        p = MachO(path)
        return True
    except ValueError as e:
        # Grrr, why isn't macholib raising proper exceptions...
        assert str(e).startswith("Unknown Mach-O")
        return False

def is_executable(path):
    """Return True if the given file is a mach-o file of type 'execute'."""
    return _is_macho_type(path, "execute")

def is_dylib(path):
    """Return True if the given file is a mach-o file of type 'execute'."""
    return _is_macho_type(path, "dylib")

def is_bundle(path):
    """Return True if the given file is a mach-o file of type 'bundle'."""
    return _is_macho_type(path, "bundle")
