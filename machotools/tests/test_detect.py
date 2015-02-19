import unittest

from machotools.detect import is_macho, is_dylib, is_executable, is_bundle

from machotools.tests.common import (
    FOO_DYLIB, SIMPLE_MAIN, SIMPLE_BUNDLE, NO_MACHO_FILE, TINY_FILE
)

class TestDetect(unittest.TestCase):
    def test_tiny_file(self):
        self.assertFalse(is_macho(TINY_FILE))

    def test_dylib(self):
        self.assertTrue(is_dylib(FOO_DYLIB))
        self.assertFalse(is_bundle(FOO_DYLIB))
        self.assertFalse(is_executable(FOO_DYLIB))

    def test_bundle(self):
        self.assertFalse(is_dylib(SIMPLE_BUNDLE))
        self.assertTrue(is_bundle(SIMPLE_BUNDLE))
        self.assertFalse(is_executable(SIMPLE_BUNDLE))

    def test_executable(self):
        self.assertFalse(is_dylib(SIMPLE_MAIN))
        self.assertFalse(is_bundle(SIMPLE_MAIN))
        self.assertTrue(is_executable(SIMPLE_MAIN))

    def test_no_macho(self):
        self.assertFalse(is_dylib(NO_MACHO_FILE))
        self.assertFalse(is_bundle(NO_MACHO_FILE))
        self.assertFalse(is_executable(NO_MACHO_FILE))

    def test_is_macho(self):
        self.assertTrue(is_macho(FOO_DYLIB))
        self.assertTrue(is_macho(SIMPLE_MAIN))
        self.assertTrue(is_macho(SIMPLE_BUNDLE))
        self.assertFalse(is_macho(NO_MACHO_FILE))
