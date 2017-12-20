import atexit as _atexit
from .backend import WIMBackend as _WIMBackend

__version__ = "0.0.0"

_backend = _WIMBackend()
ENCODING = _backend.encoding

from .error import WIMError, set_error_printing, set_error_file_name
from ._global import *
import compression
# from .file import WIMFile, WIMInfo
# from .image import WIMImage

_atexit.register(global_cleanup)
