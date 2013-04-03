Machoutils is a small set of tools built on top of macholib to retrieve and
change informations about mach-o files

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

Development happens on `github <http://github.com/enthought/machotools>`_

TODO:

        - support for multi arch
        - more detailed output for list_libraries (including versioning info)
        - add OO API
