import unittest

import os.path as op

from machotools.detect import is_macho, is_dylib, is_executable, is_bundle

from machotools.tests.common import DYLIB_DIRECTORY, FILES_TO_INSTALL_NAME
from machotools.tests.common import BaseMachOCommandTestCase

DYLIB_FILE = op.join(DYLIB_DIRECTORY, "foo.dylib")
EXECUTABLE_FILE = op.join(DYLIB_DIRECTORY, "main")
BUNDLE_FILE = op.join(DYLIB_DIRECTORY, "foo.bundle")

NO_MACHO_FILE = op.join(DYLIB_DIRECTORY, "Makefile")

class TestDetect(unittest.TestCase):
    def test_dylib(self):
        self.assertTrue(is_dylib(DYLIB_FILE))
        self.assertFalse(is_bundle(DYLIB_FILE))
        self.assertFalse(is_executable(DYLIB_FILE))

    def test_bundle(self):
        self.assertFalse(is_dylib(BUNDLE_FILE))
        self.assertTrue(is_bundle(BUNDLE_FILE))
        self.assertFalse(is_executable(BUNDLE_FILE))

    def test_executable(self):
        self.assertFalse(is_dylib(EXECUTABLE_FILE))
        self.assertFalse(is_bundle(EXECUTABLE_FILE))
        self.assertTrue(is_executable(EXECUTABLE_FILE))

    def test_no_macho(self):
        self.assertFalse(is_dylib(NO_MACHO_FILE))
        self.assertFalse(is_bundle(NO_MACHO_FILE))
        self.assertFalse(is_executable(NO_MACHO_FILE))

    def test_is_macho(self):
        self.assertTrue(is_macho(DYLIB_FILE))
        self.assertTrue(is_macho(EXECUTABLE_FILE))
        self.assertTrue(is_macho(BUNDLE_FILE))
        self.assertFalse(is_macho(NO_MACHO_FILE))
