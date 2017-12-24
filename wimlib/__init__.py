import atexit as _atexit
from wimlib.backend import WIMBackend as _WIMBackend

__version__ = "0.0.0"

_backend = _WIMBackend()
ENCODING = _backend.encoding

from wimlib.error import WIMError
import wimlib.compression as compression
import wimlib.info as info
import wimlib.image as image
import wimlib.file as file
from wimlib._global import *


_atexit.register(global_cleanup)
