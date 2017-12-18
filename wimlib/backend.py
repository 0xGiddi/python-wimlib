import cffi
import platform


# C wimlib defenitions
# All function, unions and structs are as defined in wimlib.h
# enums are defined only with a max value for silencing cffi warnings.
WIMLIB_DEFAULT_CDEFS="""
int wimlib_global_init(int init_flags);
void wimlib_global_cleanup(void);
"""

class WIMBackend(object):
	"""
	WIMBackend

	This class creates the ffi and lib objects used by other wimlib classes.
	This class is for internal use only.
	"""

	def __init__(self):
		self.os_family = platform.system()
		self.ffi = cffi.FFI()
		# Add OS specific C wimlib declarations
		# This due to diffrence between Windows and Linux wimlib_tchar defenition
		self.ffi.cdef(self._get_platform_cdefs())
		# Add default C wimlib declarations
		self.ffi.cdef(WIMLIB_DEFAULT_CDEFS)
		self.lib = self.ffi.dlopen(self._get_wimlib_path())
		self.encoding = self._get_platform_encoding()

	def _get_platform_encoding(self):
		if self.os_family == "Windows":
			return "utf-16-le"
		return "utf-8"


	def _get_platform_cdefs(self):
		if self.os_family == "Windows":
			# wimlib_tchar is a 'wchar' on windows
			return "typedef wchar_t wimlib_tchar;"
		# on any other platforms is a 'char'
		return "typedef char wimlib_tchar;"

	def _get_wimlib_path(self):
		if self.os_family == "Linux":
			return "/usr/lib/libwim.so"
		elif self.os_family == "Darwin":
			pass
		elif self.os_family == "Windows":
			pass

		raise NotImplementedError("The current platform is not recognized by wimlib ({0}, {1}).".format(self.os_family, platform.architecture()))
