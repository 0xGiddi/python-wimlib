from wimlib import _backend

ERR_SUCCESS                            = 0
ERR_ALREADY_LOCKED                     = 1
ERR_DECOMPRESSION                      = 2
ERR_FUSE                               = 6
ERR_GLOB_HAD_NO_MATCHES                = 8
ERR_ICONV_NOT_AVAILABLE                = 9
ERR_IMAGE_COUNT                        = 10
ERR_IMAGE_NAME_COLLISION               = 11
ERR_INSUFFICIENT_PRIVILEGES            = 12
ERR_INTEGRITY                          = 13
ERR_INVALID_CAPTURE_CONFIG             = 14
ERR_INVALID_CHUNK_SIZE                 = 15
ERR_INVALID_COMPRESSION_TYPE           = 16
ERR_INVALID_HEADER                     = 17
ERR_INVALID_IMAGE                      = 18
ERR_INVALID_INTEGRITY_TABLE            = 19
ERR_INVALID_LOOKUP_TABLE_ENTRY         = 20
ERR_INVALID_METADATA_RESOURCE          = 21
ERR_INVALID_MULTIBYTE_STRING           = 22
ERR_INVALID_OVERLAY                    = 23
ERR_INVALID_PARAM                      = 24
ERR_INVALID_PART_NUMBER                = 25
ERR_INVALID_PIPABLE_WIM                = 26
ERR_INVALID_REPARSE_DATA               = 27
ERR_INVALID_RESOURCE_HASH              = 28
ERR_INVALID_UTF16_STRING               = 30
ERR_INVALID_UTF8_STRING                = 31
ERR_IS_DIRECTORY                       = 32
ERR_IS_SPLIT_WIM                       = 33
ERR_LIBXML_UTF16_HANDLER_NOT_AVAILABLE = 34
ERR_LINK                               = 35
ERR_METADATA_NOT_FOUND                 = 36
ERR_MKDIR                              = 37
ERR_MQUEUE                             = 38
ERR_NOMEM                              = 39
ERR_NOTDIR                             = 40
ERR_NOTEMPTY                           = 41
ERR_NOT_A_REGULAR_FILE                 = 42
ERR_NOT_A_WIM_FILE                     = 43
ERR_NOT_PIPABLE                        = 44
ERR_NO_FILENAME                        = 45
ERR_NTFS_3G                            = 46
ERR_OPEN                               = 47
ERR_OPENDIR                            = 48
ERR_PATH_DOES_NOT_EXIST                = 49
ERR_READ                               = 50
ERR_READLINK                           = 51
ERR_RENAME                             = 52
ERR_REPARSE_POINT_FIXUP_FAILED         = 54
ERR_RESOURCE_NOT_FOUND                 = 55
ERR_RESOURCE_ORDER                     = 56
ERR_SET_ATTRIBUTES                     = 57
ERR_SET_REPARSE_DATA                   = 58
ERR_SET_SECURITY                       = 59
ERR_SET_SHORT_NAME                     = 60
ERR_SET_TIMESTAMPS                     = 61
ERR_SPLIT_INVALID                      = 62
ERR_STAT                               = 63
ERR_UNEXPECTED_END_OF_FILE             = 65
ERR_UNICODE_STRING_NOT_REPRESENTABLE   = 66
ERR_UNKNOWN_VERSION                    = 67
ERR_UNSUPPORTED                        = 68
ERR_UNSUPPORTED_FILE                   = 69
ERR_WIM_IS_READONLY                    = 71
ERR_WRITE                              = 72
ERR_XML                                = 73
ERR_WIM_IS_ENCRYPTED                   = 74
ERR_WIMBOOT                            = 75
ERR_ABORTED_BY_PROGRESS                = 76
ERR_UNKNOWN_PROGRESS_STATUS            = 77
ERR_MKNOD                              = 78
ERR_MOUNTED_IMAGE_IS_BUSY              = 79
ERR_NOT_A_MOUNTPOINT                   = 80
ERR_NOT_PERMITTED_TO_UNMOUNT           = 81


class WIMError(Exception):
        """
        Common base class for all wimlib exceptions.
        """
        def __init__(self, error):
                """
                :param error: wimlib error number or string
                :type error: string containing excepion message
                :type error: int from WIMError constants (defined as WIMLIB_ERR_* in wimlib.h)
                """
                self.errno = error
                if type(error) == int:
                        self.errno = error
                        super(WIMError, self).__init__(WIMError.getErrorString(self.errno))
                else:
                        super(WIMError, self).__init__(self.errno)


        @staticmethod
        def getErrorString(errno):
                """
                Retrive human readable error dtring from WIMLIB_ERR_* consts.

                :returns: string containing error message
                :raise ValueError: when WIMLIB_ERR_* is invalid and overflowes.
                """
                try:
                        return _backend.ffi.string(_backend.lib.wimlib_get_error_string(errno))
                except OverflowError:
                        raise ValueError("Invalid WIMLIB_ERR_* number, Please use WIMError constants.")

getErrorString = WIMError.getErrorString

def setErrorPrinting(state):
        """ Enable/Disable error and warining printing to console."""
        ret = _backend.lib.wimlib_set_print_errors(bool(state))
        if ret:
                raise WIMError(ret)

def setErrorFileName(file_path):
        """ Enable error/warning logging to specified file path."""
        ret = _backend.lib.wimlib_set_error_file_by_name(file_path)
        if ret:
                raise WIMError(ret)

def setErrorFileHandle(file_handle):
        """ Enable error/warning logging to specified FILE object"""
        raise NotImplementedError("This function is not implemented. Try setErrorFileName to log errors.")