import shutil
import tempfile
import unittest

import os.path as op

from ..rpath import add_rpaths, list_rpaths

from machotools.tests.common import DYLIB_DIRECTORY, FILES_TO_RPATHS

class TestRpath(unittest.TestCase):
    def _save_temp_copy(self, filename):
        temp_fp = tempfile.NamedTemporaryFile()
        with open(filename, "rb") as fp:
            shutil.copyfileobj(fp, temp_fp)

        return temp_fp

    def test_list_rpaths(self):
        for f, rpaths in FILES_TO_RPATHS.items():
            self.assertEqual(len(list_rpaths(f)), 1)
            self.assertEqual(list_rpaths(f)[0], rpaths)

    def test_write_rpath_empty(self):
        r_rpaths = ["@loader_path/../lib"]

        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")
        temp_fp = self._save_temp_copy(dylib)
        add_rpaths(temp_fp.name, r_rpaths)

        self.assertEqual(list_rpaths(temp_fp.name)[0], r_rpaths)

    def test_write_rpath_existing(self):
        dylib = op.join(DYLIB_DIRECTORY, "foo_rpath.dylib")
        new_rpath = "@loader_path/../lib2"

        r_rpaths = list_rpaths(dylib)[0]
        r_rpaths.append(new_rpath)

        temp_fp = tempfile.NamedTemporaryFile()
        with open(dylib, "rb") as fp:
            shutil.copyfileobj(fp, temp_fp)

        add_rpaths(temp_fp.name, [new_rpath])

        self.assertEqual(list_rpaths(temp_fp.name)[0], r_rpaths)
