import unittest

import os.path as op

import machotools.misc

DYLIB_DIRECTORY = op.join(op.dirname(__file__), "data")

FILES_TO_INSTALL_NAME = {
    op.join(DYLIB_DIRECTORY, "foo.dylib"): "foo.dylib",
    op.join(DYLIB_DIRECTORY, "foo2.dylib"): "yoyo.dylib",
}

class TestInstallName(unittest.TestCase):
    def test_simple(self):
        for f, install_name in FILES_TO_INSTALL_NAME.iteritems():
            self.assertEqual(len(machotools.misc.install_name(f)), 1)
            self.assertEqual(machotools.misc.install_name(f)[0], install_name)
