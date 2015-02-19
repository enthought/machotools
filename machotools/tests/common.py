import contextlib
import shutil
import tempfile
import unittest

import os.path as op

import macholib

DYLIB_DIRECTORY = op.join(op.dirname(__file__), "data")

FOO_DYLIB = op.join(DYLIB_DIRECTORY, "foo.dylib")
FILES_TO_INSTALL_NAME = {
    FOO_DYLIB: "foo.dylib",
    op.join(DYLIB_DIRECTORY, "foo2.dylib"): "yoyo.dylib",
}

FILES_TO_RPATHS = {
    FOO_DYLIB: [],
    op.join(DYLIB_DIRECTORY, "foo_rpath.dylib"): ["@loader_path/../lib"],
}

SIMPLE_MAIN = op.join(DYLIB_DIRECTORY, "main")
FILES_TO_DEPENDENCY_NAMES = {
    SIMPLE_MAIN: ["bar.1.0.0.dylib", "/usr/lib/libSystem.B.dylib"]
}

SIMPLE_BUNDLE = op.join(DYLIB_DIRECTORY, "foo.bundle")

NO_MACHO_FILE = op.join(DYLIB_DIRECTORY, "Makefile")

TINY_FILE = op.join(DYLIB_DIRECTORY, "tiny")

@contextlib.contextmanager
def mkdtemp():
    d = tempfile.mkdtemp()
    yield d
    shutil.rmtree(d)

class BaseMachOCommandTestCase(unittest.TestCase):
    def assert_commands_equal(self, filename, r_filename, filters=None):
        """Check that the mach-o header commands are the same in filename and
        r_filename, except for the commands which id are in filter_ids."""
        if filters is None:
            filters = {}

        r_m = macholib.MachO.MachO(r_filename)
        m = macholib.MachO.MachO(filename)

        # We don't really support multi-arch mach-o for now
        self.assertEqual(len(r_m.headers), 1)
        self.assertEqual(len(r_m.headers), len(m.headers))

        r_header = r_m.headers[0]
        header = m.headers[0]

        self.assertEqual(len(r_header.commands), len(header.commands))
        for r_cmd, cmd in zip(r_header.commands, header.commands):
            filter = filters.get(r_cmd[0].cmd, lambda x: x)
            self.assertEqual(filter(r_cmd), filter(cmd))

