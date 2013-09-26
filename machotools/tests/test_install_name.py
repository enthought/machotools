import shutil
import tempfile
import unittest

import os.path as op

from macholib import mach_o

from .. import dependency, misc
from .common import DYLIB_DIRECTORY, FILES_TO_INSTALL_NAME
from .common import BaseMachOCommandTestCase

class TestInstallName(BaseMachOCommandTestCase):
    def test_simple_read(self):
        for f, install_name in FILES_TO_INSTALL_NAME.items():
            self.assertEqual(len(misc.install_name(f)), 1)
            self.assertEqual(misc.install_name(f)[0], install_name)

    def test_simple_write(self):
        r_install_name = "youpla.dylib"

        temp_fp = tempfile.NamedTemporaryFile()
        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")
        with open(dylib, "rb") as fp:
            shutil.copyfileobj(fp, temp_fp)

        misc.change_install_name(temp_fp.name, r_install_name)

        self.assertEqual(misc.install_name(temp_fp.name)[0], r_install_name)
        filters = {mach_o.LC_ID_DYLIB: lambda x: (x[0], x[1])}
        self.assert_commands_equal(dylib, temp_fp.name, filters)

class TestDependents(unittest.TestCase):
    def test_simple(self):
        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")

        self.assertEqual(len(dependency.dependencies(dylib)), 1)
        self.assertEqual(dependency.dependencies(dylib)[0], ["/usr/lib/libSystem.B.dylib"])
