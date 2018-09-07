from wimlib import compression, _backend
import uuid

CHANGE_READONLY_FLAG = 0x00000001
CHANGE_GUID = 0x00000002
CHANGE_BOOT_INDEX = 0x00000004
CHANGE_RPFIX_FLAG = 0x00000008

class Info(object):
    def __init__(self, info_struct=None):
        if not info_struct:
            self._info_struct = _backend.ffi.new("struct wimlib_wim_info*")
        else:
            self._info_struct = info_struct

    @property
    def compression_type(self):
        return (self._info_struct.compression_type, compression.get_compression_type_string(self._info_struct.compression_type))

    @property
    def boot_index(self):
        return self._info_struct.boot_index

    @boot_index.setter
    def boot_index(self, value):
        if 0 < value <= self.image_count:
            self._info_struct.boot_index = value
        else:
            raise ValueError("Image {0} does not exist. (Valid values: 0 < value <= {1})".format(value, self.image_count))

    @property
    def chunk_size(self):
        return self._info_struct.chunk_size

    @property
    def guid(self):
        return uuid.UUID(bytes=[chr(self._info_struct.guid[i]) for i in xrange(16)])

    @guid.setter
    def guid(self, value):
        if type(value) is not uuid.UUID:
            raise ValueError("GUID should be of type UUID")
        self._info_struct.guid = value.get_bytes()

    @property
    def has_integrity_table(self):
        return self._info_struct.has_integrity_table

    @property
    def has_rpfix(self):
        return bool(self._info_struct.has_rpfix)

    @has_rpfix.setter
    def has_rpfix(self, value):
        try:
            self._info_struct.has_rpfix = int(value)
        except ValueError:
            raise ValueError("has_rpfix should be of type bool.")

    @property
    def image_count(self):
        return self._info_struct.image_count

    @property
    def read_only_flag(self):
        return bool(self._info_struct.is_marked_readonly)

    @read_only_flag.setter
    def read_only_flag(self, value):
        try:
            self._info_struct.is_marked_readonly = int(value)
        except ValueError:
            raise ValueError("hasReadOnlyFlag should be of type bool.")

    @property
    def is_read_only(self):
		"""
		True if this WIM file is considered readonly for any reason
		(e.g. "readonly" header flag, split WIM, filesystem permissions)
		"""
		return bool(self._info_struct.is_readonly)

    @property
    def metadata_only_flag(self):
		"""True if the "metadata only" flag is set in this WIM's header"""
		return bool(self._info_struct.metadata_only)

    @property
    def opened_from_file(self):
		""" True if this info struct is for a WIMStruct that has a backing file  """
		return bool(self._info_struct.opened_from_file)

    @property
    def part_number(self):
		""" For split WIMs, the 1-based index of this part within the split WIM; otherwise 1. """
		return self._info_struct.part_number

    @property
    def is_pipeable(self):
		"""True if this WIM file is pipable (see WIMLIB_WRITE_FLAG_PIPABLE)"""
		return bool(self._info_struct.pipable)

    @property
    def resource_only_flag(self):
		""" True if the "resource only" flag is set in this WIM's header """
		return self._info_struct.resource_only

    @property
    def is_spanned(self):
		""" True if the "spanned" flag is set in this WIM's header """
		return bool(self._info_struct.spanned)

    @property
    def total_bytes(self):
		""" The size of this WIM file in bytes, excluding the XML data and integrity table. """
		return self._info_struct.total_bytes

    @property
    def total_parts(self):
		""" For split WIMs, the total number of parts in the split WIM; otherwise 1. """
		return self._info_struct.total_parts

    @property
    def wim_version(self):
		""" The version of the WIM file format used in this WIM file. """
		return self._info_struct.wim_version

    @property
    def write_in_progress_flag(self):
		""" True if  the "write in progress" flag is set in this WIM's header. """
		return bool(self._info_struct.write_in_progress)
