import shutil
import tempfile
import unittest

import os.path as op

import macholib
from macholib import mach_o

import machotools

from machotools.tests.common import DYLIB_DIRECTORY, FILES_TO_INSTALL_NAME

class TestInstallName(unittest.TestCase):
    def _assert_commands_equal(self, filename, r_filename, filters=None):
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

    def test_simple_read(self):
        for f, install_name in FILES_TO_INSTALL_NAME.iteritems():
            self.assertEqual(len(machotools.install_name(f)), 1)
            self.assertEqual(machotools.install_name(f)[0], install_name)

    def test_simple_write(self):
        r_install_name = "youpla.dylib"

        temp_fp = tempfile.NamedTemporaryFile()
        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")
        with open(dylib, "rb") as fp:
            shutil.copyfileobj(fp, temp_fp)

        machotools.change_install_name(temp_fp.name, r_install_name)

        self.assertEqual(machotools.install_name(temp_fp.name)[0], r_install_name)
        filters = {mach_o.LC_ID_DYLIB: lambda x: (x[0], x[1])}
        self._assert_commands_equal(dylib, temp_fp.name, filters)

class TestDependents(unittest.TestCase):
    def test_simple(self):
        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")

        self.assertEqual(len(machotools.dependencies(dylib)), 1)
        self.assertEqual(machotools.dependencies(dylib)[0], ["/usr/lib/libSystem.B.dylib"])
