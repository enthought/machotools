import shutil
import unittest

import os.path as op

from .. import dependency, misc
from ..macho_rewriter import DylibRewriter, ExecutableRewriter, \
    _MachoRewriter, rewriter_factory
from ..rpath import list_rpaths
from ..tests.common import FILES_TO_DEPENDENCY_NAMES, FILES_TO_RPATHS, \
    FILES_TO_INSTALL_NAME, FOO_DYLIB, SIMPLE_MAIN, mkdtemp

class TestMachoRewriter(unittest.TestCase):
    def test_rpaths(self):
        for f, r_rpaths in FILES_TO_RPATHS.items():
            rewriter = _MachoRewriter(f)
            self.assertEqual(rewriter.rpaths, r_rpaths)

    def test_context_manager(self):
        with mkdtemp() as d:
            for f, r_rpaths in FILES_TO_RPATHS.items():
                copy = op.join(d, op.basename(f))
                shutil.copy(f, copy)

                with _MachoRewriter(copy) as rewriter:
                    rewriter.append_rpath("yomama")

                self.assertEqual(list_rpaths(copy)[0], r_rpaths + ["yomama"])

    def test_append_rpath(self):
        with mkdtemp() as d:
            for f, r_rpaths in FILES_TO_RPATHS.items():
                copy = op.join(d, op.basename(f))
                shutil.copy(f, copy)

                rewriter = _MachoRewriter(copy)
                rewriter.append_rpath("yomama")

                self.assertEqual(rewriter.rpaths, r_rpaths + ["yomama"])

                rewriter.commit()
                self.assertEqual(list_rpaths(copy)[0], r_rpaths + ["yomama"])

    def test_extend_rpaths(self):
        with mkdtemp() as d:
            for f, r_rpaths in FILES_TO_RPATHS.items():
                appended_rpaths = ["yomama", "yoyoma"]

                copy = op.join(d, op.basename(f))
                shutil.copy(f, copy)

                rewriter = _MachoRewriter(copy)
                rewriter.extend_rpaths(appended_rpaths)

                self.assertEqual(rewriter.rpaths, r_rpaths + appended_rpaths)

                rewriter.commit()
                self.assertEqual(list_rpaths(copy)[0], r_rpaths + appended_rpaths)

    def test_append_rpath_if_not_exist(self):
        with mkdtemp() as d:
            for f, r_rpaths in FILES_TO_RPATHS.items():
                copy = op.join(d, op.basename(f))
                shutil.copy(f, copy)

                rewriter = _MachoRewriter(copy)
                rewriter.append_rpath("yomama")
                rewriter.append_rpath_if_not_exists("yomama")

                self.assertEqual(rewriter.rpaths, r_rpaths + ["yomama"])

                rewriter.commit()
                self.assertEqual(list_rpaths(copy)[0], r_rpaths + ["yomama"])

                rewriter.append_rpath_if_not_exists("yemama")
                rewriter.commit()

                self.assertEqual(list_rpaths(copy)[0], r_rpaths + ["yomama", "yemama"])

    def test_dependencies(self):
        for f, dependencies in FILES_TO_DEPENDENCY_NAMES.items():
            rewriter = _MachoRewriter(f)
            self.assertEqual(rewriter.dependencies, dependencies)

    def test_change_dependency(self):
        with mkdtemp() as d:
            r_dependencies = ["bar.2.0.0.dylib", "/usr/lib/libSystem.B.dylib"]

            main = SIMPLE_MAIN
            old_dependency = "bar.1.0.0.dylib"
            new_dependency = "bar.2.0.0.dylib"

            copy = op.join(d, op.basename(main))
            shutil.copy(main, copy)

            rewriter = _MachoRewriter(copy)
            rewriter.change_dependency(old_dependency, new_dependency)

            self.assertEqual(rewriter.dependencies, r_dependencies)

            rewriter.commit()
            self.assertEqual(dependency.dependencies(copy)[0], r_dependencies)

class TestDylibRewriter(unittest.TestCase):
    def test_install_name(self):
        for f, r_install_name in FILES_TO_INSTALL_NAME.items():
            rewriter = DylibRewriter(f)
            self.assertEqual(rewriter.install_name, r_install_name)

    def test_change_install_name(self):
        with mkdtemp() as d:
            for f, r_install_name in FILES_TO_INSTALL_NAME.items():
                copy = op.join(d, op.basename(f))
                shutil.copy(f, copy)

                rewriter = DylibRewriter(copy)
                rewriter.install_name = "yomama"

                self.assertEqual(rewriter.install_name, "yomama")

                rewriter.commit()
                self.assertEqual(misc.install_name(copy)[0], "yomama")

class TestRewriterFactory(unittest.TestCase):
    def test_simple(self):
        rewriter = rewriter_factory(SIMPLE_MAIN)
        self.assertTrue(isinstance(rewriter, ExecutableRewriter))

        rewriter = rewriter_factory(FOO_DYLIB)
        self.assertTrue(isinstance(rewriter, DylibRewriter))
