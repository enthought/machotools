import os.path as op

DYLIB_DIRECTORY = op.join(op.dirname(__file__), "data")

FILES_TO_INSTALL_NAME = {
    op.join(DYLIB_DIRECTORY, "foo.dylib"): "foo.dylib",
    op.join(DYLIB_DIRECTORY, "foo2.dylib"): "yoyo.dylib",
}

FILES_TO_RPATHS = {
    op.join(DYLIB_DIRECTORY, "foo.dylib"): [],
    op.join(DYLIB_DIRECTORY, "foo_rpath.dylib"): ["@loader_path/../lib"],
}

