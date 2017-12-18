from wimlib import _backend
from .error import WIMError

# Init flags for wimlib_global_init
INIT_FLAG_DONT_ACQUIRE_PRIVILEGES	= 0x00000002 # Windows only
INIT_FLAG_STRICT_CAPTURE_PRIVILEGES	= 0x00000004 # Windown only
INIT_FLAG_STRICT_APPLY_PRIVILEGES	= 0x00000008 # Windows only
INIT_FLAG_DEFAULT_CASE_SENSITIVE 	= 0x00000010 
INIT_FLAG_DEFAULT_CASE_INSENSITIVE	= 0x00000020

# Image specificaion consts
NO_IMAGE = 0
ALL_IMAGES = -1

# Global funcions
def global_init(init_flags=0):
	"""
	Initialization function for wimlib.

	This function should be called before any use of wimlib.
	If the function is not called before use, a automaic call
	will take place with init_flags=0.
	"""
	ret = _backend.lib.wimlib_global_init(init_flags)
	if ret:
		raise WIMError(ret)

def global_cleanup():
	"""
	Cleanup function for wimlib.
	This function is auto called by atexit.
	"""
	try:
		_backend.lib.wimlib_global_cleanup()
	except Exception as ex:
		# It's not critical if this function call fails.
		pass