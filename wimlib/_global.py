from wimlib import _backend
from .error import WIMError

# Init flags for wimlib_global_init
INIT_FLAG_DONT_ACQUIRE_PRIVILEGES = 0x00000002  # Windows only
INIT_FLAG_STRICT_CAPTURE_PRIVILEGES = 0x00000004  # Windown only
INIT_FLAG_STRICT_APPLY_PRIVILEGES = 0x00000008  # Windows only
INIT_FLAG_DEFAULT_CASE_SENSITIVE = 0x00000010
INIT_FLAG_DEFAULT_CASE_INSENSITIVE = 0x00000020

# Image specificaion consts
NO_IMAGE = 0
ALL_IMAGES = -1

def wimlib_version():
    """ Get wimlib version number as tuple of (MAJOR, MINOR, PATCH) """
    ver = _backend.lib.wimlib_get_version()
    return (ver >> 20, (ver >> 10) & 0x3ff, ver & 0x3ff)

def global_init(init_flags=0):
    """ Initialization function for wimlib, called by default with flags=0"""
    ret = _backend.lib.wimlib_global_init(flags)
    if ret:
        raise WIMError(ret)

def global_cleanup():
    """ Cleanup function for wimlib, call is optional. """
    _backend.lib.wimlib_global_cleanup()

def join():
    raise NotImplementedError()

def join_with_progress():
    raise NotImplementedError()

def set_memory_allocator():
    raise NotImplementedError()