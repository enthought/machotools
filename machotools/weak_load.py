from macholib.ptypes import (
	Structure
)
import macholib.MachO
import macholib.mach_o

from macholib.mach_o import LC_LOAD_WEAK_DYLIB, dylib
from .utils import convert_to_string


class weak_dylib_command(Structure):
	_fields_ = dylib._fields_

	def describe(self):
		s = {
			"timestamp": str(self.timestamp),
			"current_version": str(self.current_version),
			"compatibility_version": str(self.compatibility_version)
		}
		return s


def list_weak_dylibs(filename):
	"""Get the list of weak dylib defined in the given mach-o binary.

	The returned value is a list weak dylibs such as weak_dylibs[i] is the list of weak_dylib
	in the i-th header. For this to work, we have to create a new class specifically for
	LC_LOAD_WEAK_DYLIB registry

	Note
	----
	The '\0' padding at the end of each weak_dylib is stripped

	Parameters
	----------
	filename: str
		The path to the mach-o binary file to look at
	"""

	macholib.mach_o.LC_REGISTRY[LC_LOAD_WEAK_DYLIB] = weak_dylib_command
	m = macholib.MachO.MachO(filename)
	return _list_weak_dylibs_macho(m)


def _list_weak_dylibs_macho(m):
	weak_dylibs = []
	for header in m.headers:
		header_weak = []
		weak_load_commands = [command for command in header.commands if isinstance(command[1], weak_dylib_command)]
		for weak_load_command in weak_load_commands:
			weak_dylib = weak_load_command[2]
			if not weak_dylib.endswith(b"\x00"):
				raise ValueError("Unexpected end character for weak dylib command value: %r".format(weak_dylib))
			else:
				header_weak.append(convert_to_string(weak_dylib))
		weak_dylibs.append(header_weak)
	return weak_dylibs
