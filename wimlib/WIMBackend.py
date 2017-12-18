import cffi
import platform


# C wimlib defenitions
# All function, unions and structs are as defined in wimlib.h
# enums are defined only with a max value for silencing cffi warnings.
WIMLIB_DEFAULT_CDEFS="""

"""

class WIMBackend(object):
	"""
	WIMBackend

	This class creates the ffi and lib objects used by other wimlib classes.
	This class is for internal use only.
	"""

	def __init__(self):
		self.ffi = cffi.FFI()
		# Add OS specific C wimlib declarations
		# This due to diffrence between Windows and Linux wimlib_tchar defenition
		self.ffi.cdef(WIMBackend._get_platform_cdefs())
		# Add default C wimlib declarations
		self.ffi.cdef(WIMLIB_DEFAULT_CDEFS)
		self.lib = self._ffi.dlopen(WIMBackend._get_wimlib_path())
		self.encoding = WIMBackend._get_platform_encoding()

	@staticmethod
	def _get_platfom_encoding():
		if platform.system() == "Windows":
			return "utf-16-le"
		return "utf-8"


	@staticmethod
	def _get_platform_cdefs():
		if platform.system() == "Windows":
			# wimlib_tchar is a 'wchar' on windows
			return "typedef wchar_t wimlib_tchar;"
		# on any other platforms is a 'char'
		return "typedef char wimlib_tchar;"

	@staticmethod
	def _get_wimlib_path():
		os_family = platform.system()
		if os_family == "Linux":
			return "/usr/lib/libwim.so"
		elif os_family == "Darwin":
			pass
		elif os_family == "Windows":
			pass

		raise NotImplementedError("The current platform is not recognized by wimlib ({0}, {1}).".format(platform.system(), platform.architecture()))
