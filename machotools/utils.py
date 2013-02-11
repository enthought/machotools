def count_end_null_bytes(s):
    """Returns the number of NULL bytes at the end of the given string."""
    if s.endswith(b'\x00'):
        i = 1
        while s[-i] == b'\x00':
            i += 1
        return i - 1
    else:
        return 0

def rstrip_null_bytes(s):
    """Right-strip any null bytes at the end of the given string."""
    n_null = count_end_null_bytes(s) 
    if n_null > 0:
        return s[:-n_null]
    else:
        return s
