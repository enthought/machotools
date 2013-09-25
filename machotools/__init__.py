# Copyright (c) 2013 by Enthought, Ltd.
# All rights reserved.
__version__ = "0.1.0.dev1"

from machotools.macho_rewriter import BundleRewriter, DylibRewriter, \
    ExecutableRewriter, rewriter_factory

# Silent pyflakes vim plugin
__all__ = [
    "BundleRewriter", "DylibRewriter", "ExecutableRewriter",
    "rewriter_factory",
    "__version__",
]

from .version import __version__
