Machotools is a small set of tools built on top of macholib to retrieve and
change informations about mach-o files. Think of it as a pure python,
cross-platform implementation of install_name_tool

Examples::

        # Print the list of rpath defined in the given .dylib
        python -m machotools list_rpaths foo.dylib

        # Print the id (i.e. install_name) of the given .dylib
        python -m machotools install_name foo.dylib

        # Print the list of libraries linked in the given mach-o (simple otool
        # -L)
        python -m machotools list_libraries a.out

Internally, machotools is written as a library so that it can be used within
bigger tools, but the API is currently in-flux until the first 1.0 release.

Example::

        from machotools import rewriter_factory

        rewriter = rewriter_factory("foo.dylib")
        print rewriter.dependencies
        # install_name property only available if rewriter is a DylibRewriter
        # instance (auto-detected in rewriter_factory)
        print rewriter.install_name
        print rewriter.rpaths

        rewriter.install_name = "bar.dylib"
        # Changes are not actually written until you call commit()
        rewriter.commit()

        # When modifying a binary, one can also use context manager so that
        # changes are automatically committed when exciting the context.
        with rewriter_factory("foo.dylib") as rewriter:
            rewriter.install_name = "bar.dylib"

Main features:

        - ability to query/change rpath
        - ability to query/change the install name
        - ability to query/change the dependencies
        - should work on any platform supported by macholib (mac os x, unix,
          windows)
        - modifications are safe against crash/interruption as files are never
          modified in place. Instead, modifications are made against a
          temporary copy, and replace the original file using atomic rename on
          Posix (emulated on windows).

Development happens on `github <http://github.com/enthought/machotools>`_

TODO:

        - support for multi arch
        - more detailed output for list_libraries (including versioning info)
