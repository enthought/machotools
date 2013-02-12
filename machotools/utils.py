# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
import os
import shutil
import uuid

from macholib.util import fsencoding

def macho_path_as_data(filename, pad_to=4):
    """ Encode a path as data for a MachO header.

    Namely, this will encode the text according to the filesystem
    encoding and zero-pad the result out to 4 bytes.

    Parameters
    ----------
    filename: str
        Path string to encode
    pad_to: int
        Number of bytes to pad the encoded string to
    """
    filename = fsencoding(filename) + b'\x00'
    rem = len(filename) % pad_to
    if rem > 0:
        filename += b'\x00' * (pad_to - rem)
    return filename

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

def safe_write(target, writer, mode="wt"):
    """a 'safe' way to write to files.

    Instead of writing directly into a file, this function writes to a
    temporary file in the same directory, and then rename the file to the
    target if no error occured.  On most platforms, rename is atomic, so this
    avoids leaving stale files in inconsistent states.

    Parameters
    ----------
    target: str
        destination to write to
    writer: callable or data
        if callable, assumed to be function which takes one argument, a file
        descriptor, and writes content to it. Otherwise, assumed to be data
        to be directly written to target.
    mode: str
        opening mode
    """
    if not callable(writer):
        data = writer
        writer = lambda fp: fp.write(data)

    tmp_target = "%s.tmp%s" % (target, uuid.uuid4().hex)
    f = open(tmp_target, mode)
    try:
        writer(f)
    finally:
        f.close()
    os.rename(tmp_target, target)

def safe_update(target, writer, mode="wt"):
    """a 'safe' way to update a file.

    Instead of writing directly into a file, this function first copies target
    to a temporary file and, writes to it, and then rename the file to the
    target if no error occured.  On most platforms, rename is atomic, so this
    avoids leaving stale files in inconsistent states.

    Parameters
    ----------
    target: str
        file to update
    writer: callable or data
        if callable, assumed to be function which takes one argument, a file
        descriptor, and writes content to it. Otherwise, assumed to be data
        to be directly written to target.
    mode: str
        opening mode
    """
    if 'b' in mode:
        target_mode = 'rb'
    else:
        target_mode = 'r'

    def writer_wrap(f):
        g = open(target, target_mode)
        try:
            shutil.copyfileobj(g, f)
        finally:
            g.close()
        return writer(f)
    return safe_write(target, writer_wrap, mode)
