import re

import macholib

from .errors import MachoError
from .dependency import _list_dependencies_macho, _change_command_data_inplace, \
        _find_lc_dylib_command
from .detect import detect_macho_type
from .misc import _install_name_macho, _change_id_dylib_command
from .rpath import _add_rpath_to_header, _list_rpaths_macho
from .utils import convert_to_string, safe_update

class _MachoRewriter(object):
    """
    Macho rewriters can be used to query and change mach-o properties relevant
    for relocatability.

    Concretely, you can query/modify the following:

        - rpaths sections
        - dependencies

    See also
    --------
    rewriter_factory which instanciates the right rewriter by auto-guessing the
    mach-o type.
    """
    def __init__(self, filename):
        self.filename = filename

        self._m = macholib.MachO.MachO(filename)
        if len(self._m.headers) == 0:
            raise MachoError("No header found ?")
        elif len(self._m.headers) > 1:
            raise MachoError("Universal binaries not yet supported")

        self._rpaths = _list_rpaths_macho(self._m)[0]
        self._dependencies = _list_dependencies_macho(self._m)[0]

    def __enter__(self):
        return self

    def __exit__(self, *a, **kw):
        self.commit()

    def commit(self):
        def writer(f):
            f.seek(0)
            self._m.headers[0].write(f)
        safe_update(self.filename, writer, "wb")

    @property
    def rpaths(self):
        """
        This is the list of defined rpaths.

        Note
        ----
        This includes the list of uncommitted changes.
        """
        return self._rpaths

    #----------
    # rpath API
    #----------
    def extend_rpaths(self, new_rpaths):
        """
        Extend the existing set of rpaths with the given list.

        Parameters
        ----------
        new_rpaths: seq
            List of rpaths (i.e. list of strings).

        Note
        ----
        The binary is not actually updated intil the sync method has been
        called.
        """
        header = self._m.headers[0]
        for rpath in new_rpaths:
            self._rpaths.append(rpath)
            _add_rpath_to_header(header, rpath)

    def append_rpath(self, new_rpath):
        """
        Append the given rpath to the existing set of rpaths.

        Parameters
        ----------
        new_rpath: str
            The new rpath.

        Note
        ----
        The binary is not actually updated intil the sync method has been
        called.
        """
        header = self._m.headers[0]
        self._rpaths.append(new_rpath)
        _add_rpath_to_header(header, new_rpath)

    def append_rpath_if_not_exists(self, new_rpath):
        """
        Append the given rpath to the existing set of rpaths, but only if it
        does not already defined in the binary.

        Parameters
        ----------
        new_rpath: str
            The new rpath.

        Note
        ----
        The binary is not actually updated until the sync method has been
        called.
        """
        header = self._m.headers[0]
        if not new_rpath in self._rpaths:
            _add_rpath_to_header(header, new_rpath)

    #-----------------
    # dependencies API
    #-----------------
    @property
    def dependencies(self):
        """
        The list of dependencies.

        Note
        ----
        This includes the list of uncommitted changes.
        """
        return self._dependencies

    def change_dependency(self, old_dependency_pattern, new_dependency,
                          ignore_error=True):
        """
        Change the dependency matching the given pattern to the new dependency
        name.

        Parameters
        ----------
        old_dependency_pattern: str
            Regex pattern to match against
        new_dependency: str
            New dependency name to replace with.
        ignore_error: bool
            If true, do not raise an exception of no dependency has been
            changed.
        """
        r_old_dependency = re.compile(old_dependency_pattern)
        old_dependencies = self._dependencies[:]

        header = self._m.headers[0]

        i_dependency = 0
        for command_index, (load_command, dylib_command, data) in \
                _find_lc_dylib_command(header, macholib.mach_o.LC_LOAD_DYLIB):

            name = convert_to_string(data)
            m = r_old_dependency.search(name)
            if m:
                _change_command_data_inplace(header, command_index,
                        (load_command, dylib_command, data), new_dependency)
                self._dependencies[i_dependency] = new_dependency

            i_dependency += 1

        if not ignore_error and old_dependencies != self._dependencies:
            raise MachoError("Pattern {0} not found in the list of dependencies".
                             format(old_dependency_pattern))

class ExecutableRewriter(_MachoRewriter):
    pass

class BundleRewriter(_MachoRewriter):
    pass

class DylibRewriter(_MachoRewriter):
    def __init__(self, filename):
        super(DylibRewriter, self).__init__(filename)

        if not self._m.headers[0].filetype == "dylib":
            raise MachoError("file {0} is not a dylib".format(filename))

        self._install_name = _install_name_macho(self._m)[0]

    @property
    def install_name(self):
        return self._install_name

    @install_name.setter
    def install_name(self, new_install_name):
        _change_id_dylib_command(self._m.headers[0], new_install_name)

        self._install_name = new_install_name

def rewriter_factory(filename):
    macho_type = detect_macho_type(filename)
    if macho_type == "dylib":
        return DylibRewriter(filename)
    elif macho_type == "execute":
        return ExecutableRewriter(filename)
    elif macho_type == "bundle":
        return BundleRewriter(filename)
    else:
        raise MachoError("file {0} is not a mach-o file !".format(filename))
