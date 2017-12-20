from wimlib import _backend
from wimlib import WIMError

COMPRESSOR_FLAG_DESTRUCTIVE = 0x80000000
COMPRESSION_TYPE_NONE = 0
COMPRESSION_TYPE_XPRESS = 1
COMPRESSION_TYPE_LZX = 2
COMPRESSION_TYPE_LZMS = 3


class Compressor(object):
        """
        This class handles wimlb compressor API.
        """
        def __init__(self, ctype=0, block_size=0, level=0):
                self.ctype = ctype
                self.block_size = block_size
                self.level = level
                self._compressor = None
                self._create()

        def _create(self):
                """
                Create and populate a new wimlib_compressor.
                For internal use only.
                """
                compressor = _backend.ffi.new("struct wimlib_compressor**")
                ret = _backend.lib.wimlib_create_compressor(self.ctype, self.block_size, self.level, compressor)
                if ret:
                        raise WIMError(ret)
                self._compressor = compressor[0]

        def compress(self, in_data):
                """ Compress given data in data_in """
                if len(in_data) > self.block_size:
                        raise OverflowError("Uncompresses data should be no larger that {0}".format(self.block_size))
                out_buff = _backend.ffi.new("unsigned char[{0}]".format(self.block_size))
                out_size = _backend.lib.wimlib_compress(in_data, len(in_data), out_buff, self.block_size, self._compressor)
                return (out_size, bytes(_backend.ffi.buffer(out_buff, out_size)))

        def _free(self):
                """ Free he wimlib_compressor for the current compressor instance"""
                _backend.lib.wimlib_free_compressor(self._compressor)

        @staticmethod
        def needed_memory(ctype, block_size, level):
                """ Calculate needed memory for compression operation"""
                ret = _backend.lib.wimlib_get_compressor_needed_memory(ctype, block_size, level)
                if not ret:
                        raise Exception("Compression type or block size are incorrect")

        def __del__(self):
                self._free()


class Decompressor(object):
        def __init__(self, ctype=0, block_size=0):
                self.ctype = ctype
                self.block_size = block_size
                self.decompressor = None
                self._create()

        def _create(self):
                """
                Create and populate wimlib_decompressor.
                For internal use only
                """
                decomp = _backend.ffi.new("struct wimlib_decompressor **")
                ret = _backend.lib.wimlib_create_decompressor(self.ctype, self.block_size, decomp)
                if ret:
                        raise WIMError(ret)
                self._decompressor = decomp[0]

        def decompress(self, in_data, out_size):
                """
                Decompress a compressed data string.

                :param in_data: The data to be decompressed
                :param out_size: The size of the decompressed data
                """
                out_buff = _backend.ffi.new("unsigned char[{0}]".format(out_size))
                ret = _backend.lib.wimlib_decompress(in_data, len(in_data), out_buff, out_size, self._decompressor)
                if ret:
                        raise WIMError(ret)
                return bytes(_backend.ffi.buffer(out_buff, out_size))

        def _free(self):
                """ Free wimlib_decompressor for this instance """
                _backend.lib.wimlib_free_decompressor(self._decompressor)

        def __del__(self):
                self._free()


def set_default_level(ctype, level):
        """
        Set the default compression level for a given compression type
        This will affect any compression operations with compression_level=0.
        """
        ret = _backend.lib.wimlib_set_default_compression_level(ctype, level)
        if ret:
                raise WIMError(ret)


def get_type_string(ctype):
        """ Get string name of compression type const"""
        try:
                return _backend.ffi.string(_backend.lib.wimlib_get_compression_type_string(ctype))
        except OverflowError:
                return "Invalid"
