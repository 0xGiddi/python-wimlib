from wimlib import _backend


class WIMError(Exception):
        """
        Common base class for all wimlib exceptions.
        """
        SUCCESS                            = 0
        ALREADY_LOCKED                     = 1
        DECOMPRESSION                      = 2
        FUSE                               = 6
        GLOB_HAD_NO_MATCHES                = 8
        ICONV_NOT_AVAILABLE                = 9
        IMAGE_COUNT                        = 10
        IMAGE_NAME_COLLISION               = 11
        INSUFFICIENT_PRIVILEGES            = 12
        INTEGRITY                          = 13
        INVALID_CAPTURE_CONFIG             = 14
        INVALID_CHUNK_SIZE                 = 15
        INVALID_COMPRESSION_TYPE           = 16
        INVALID_HEADER                     = 17
        INVALID_IMAGE                      = 18
        INVALID_INTEGRITY_TABLE            = 19
        INVALID_LOOKUP_TABLE_ENTRY         = 20
        INVALID_METADATA_RESOURCE          = 21
        INVALID_MULTIBYTE_STRING           = 22
        INVALID_OVERLAY                    = 23
        INVALID_PARAM                      = 24
        INVALID_PART_NUMBER                = 25
        INVALID_PIPABLE_WIM                = 26
        INVALID_REPARSE_DATA               = 27
        INVALID_RESOURCE_HASH              = 28
        INVALID_UTF16_STRING               = 30
        INVALID_UTF8_STRING                = 31
        IS_DIRECTORY                       = 32
        IS_SPLIT_WIM                       = 33
        LIBXML_UTF16_HANDLER_NOT_AVAILABLE = 34
        LINK                               = 35
        METADATA_NOT_FOUND                 = 36
        MKDIR                              = 37
        MQUEUE                             = 38
        NOMEM                              = 39
        NOTDIR                             = 40
        NOTEMPTY                           = 41
        NOT_A_REGULAR_FILE                 = 42
        NOT_A_WIM_FILE                     = 43
        NOT_PIPABLE                        = 44
        NO_FILENAME                        = 45
        NTFS_3G                            = 46
        OPEN                               = 47
        OPENDIR                            = 48
        PATH_DOES_NOT_EXIST                = 49
        READ                               = 50
        READLINK                           = 51
        RENAME                             = 52
        REPARSE_POINT_FIXUP_FAILED         = 54
        RESOURCE_NOT_FOUND                 = 55
        RESOURCE_ORDER                     = 56
        SET_ATTRIBUTES                     = 57
        SET_REPARSE_DATA                   = 58
        SET_SECURITY                       = 59
        SET_SHORT_NAME                     = 60
        SET_TIMESTAMPS                     = 61
        SPLIT_INVALID                      = 62
        STAT                               = 63
        UNEXPECTED_END_OF_FILE             = 65
        UNICODE_STRING_NOT_REPRESENTABLE   = 66
        UNKNOWN_VERSION                    = 67
        UNSUPPORTED                        = 68
        UNSUPPORTED_FILE                   = 69
        WIM_IS_READONLY                    = 71
        WRITE                              = 72
        XML                                = 73
        WIM_IS_ENCRYPTED                   = 74
        WIMBOOT                            = 75
        ABORTED_BY_PROGRESS                = 76
        UNKNOWN_PROGRESS_STATUS            = 77
        MKNOD                              = 78
        MOUNTED_IMAGE_IS_BUSY              = 79
        NOT_A_MOUNTPOINT                   = 80
        NOT_PERMITTED_TO_UNMOUNT           = 81

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
