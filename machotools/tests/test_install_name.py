import shutil
import tempfile
import unittest

import os.path as op

import machotools

from machotools.tests.common import DYLIB_DIRECTORY, FILES_TO_INSTALL_NAME

class TestInstallName(unittest.TestCase):
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

class TestDependents(unittest.TestCase):
    def test_simple(self):
        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")

        self.assertEqual(len(machotools.dependencies(dylib)), 1)
        self.assertEqual(machotools.dependencies(dylib)[0], ["/usr/lib/libSystem.B.dylib"])
