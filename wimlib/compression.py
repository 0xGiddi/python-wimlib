from wimlib import _backend

COMPRESSOR_FLAG_DESTRUCTIVE = 0x80000000
COMPRESSION_TYPE_NONE = 0
COMPRESSION_TYPE_XPRESS = 1
COMPRESSION_TYPE_LZX = 2
COMPRESSION_TYPE_LZMS = 3


class Compressor(object):
	def __init__(self, ctype=0, block_size=0, level=0):
		self.ctype=ctype
		self.block_size = block_size
		self.level = level
		self._compressor = _backend.ffi.new("struct wimlib_compressor **")

	def compress(self, data):
		_backend.lib.wimlib_compress(data, len(data), None, None, self._compressor)

	def _free(self):
		_backend.lib.wimlib_free_compressor(self._compressor)

	@staticmethod
	def needed_memory(ctype, block_size, level):
		ret = _backend.lib.wimlib_get_compressor_needed_memory(ctype, block_size, level)
		if not ret:
			raise Exception("Compression type or block size are incorrect")

	def __del__(self):
		self._free()




class Decompressor(object):
	def __init__(self, ctype=0, block_size=0):
		self._decompressor = _backend.ffi.new("struct wimlib_decompressor **")

	def decompress(self, data):
		pass

	def _free(self):
		_backend.lib.wimlib_free_decompressor(self._decompressor)

	def __del__(self):
		self._free()

def set_default_compression_level(ctype, level):
	"""
	Set the default compression level for a given compression type
	This will affect any compression operations with compression_level=0.
	"""
	ret = _backend.lib.wimlib_set_default_compression_level(ctype, level)
	if ret:
		raise WIMError(ret)

def get_compression_name(ctype):
	""" Get string name of scompression type const"""
	try:
		return _backend.ffi.string(_backend.lib.wimlib_get_compression_type_string(ctype))
	except OverflowError:
		return "Invalid"

