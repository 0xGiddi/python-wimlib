from .WIMBackend import WIMBackend as _WIMBackend

__version__ == "0.0.0"

_backend = _WIMBackend()
ENCODING = _backend.encoding


