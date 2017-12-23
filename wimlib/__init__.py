import atexit as _atexit
from wimlib.backend import WIMBackend as _WIMBackend

__version__ = "0.0.0"

_backend = _WIMBackend()
ENCODING = _backend.encoding

from wimlib.error import WIMError
from wimlib._global import *
import wimlib.compression
#import wimlib.progress
from wimlib.info import *
from wimlib.image import *
from wimlib.file import *
# from .file import WIMFile, WIMInfo
# from .image import WIMImage

_atexit.register(global_cleanup)
