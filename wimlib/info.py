from wimlib import compression, _backend
import uuid

CHANGE_READONLY_FLAG = 0x00000001
CHANGE_GUID = 0x00000002
CHANGE_BOOT_INDEX = 0x00000004
WIMLIB_CHANGE_RPFIX_FLAG = 0x00000008


class WIMInfo(object):
	def __init__(self, wim_struct):
		self._wim_struct = wim_struct
		self._wim_info = _backend.ffi.new("struct wimlib_wim_info *")
		ret = _backend.lib.wimlib_get_wim_info(self._wim_struct, self._wim_info)
		if ret:
			raise WIMError(ret)

	def write(self, flags):
		ret = _backend.lib.wimlib_set_wim_info(self._wim_struct, self._wim_info, flags)
		if ret:
			raise WIMError(ret)


	@property
	def compression_type(self):
		"""
		The default compression type of resources in this WIM file, 
		as one of the WIMCompression constants.
		"""
		return (self._wim_info.compression_type, compression.get_type_string(self._wim_info.compression_type))

	@property
	def boot_index(self):
		"""
		The 1-based index of the bootable image in this WIM file, 
		or 0 if no image is bootable. 
		"""
		return self._wim_info.boot_index

	@boot_index.setter
	def boot_index(self, value):
		if 0 < value <= self.image_count:
			self._wim_info.boot_index = value
		else:
			raise ValueError("Image {0} does not exist. (Valid values: 0 < value <= {1})".format(value, self.image_count))

	@property
	def chunk_size(self):
		"""The default compression chunk size of resources in this WIM file."""
		return self._wim_info.chunk_size

	@property
	def guid(self):
		"""
		The globally unique identifier for this WIM.
		(Note: all parts of a split WIM normally have identical GUIDs.)
		"""
		return uuid.UUID(bytes=[chr(self._wim_info.guid[i]) for i in xrange(16)])


	@guid.setter
	def guid(self, value):
		if type(value) is not uuid.UUID:
			raise ValueError("GUID should be of type UUID")
		self._wim_info.guid = value.get_bytes()

	@property
	def has_integrity_table(self):
		"""True if this WIM file has an integrity table."""
		return self._wim_info.has_integrity_table

	@property
	def has_rpfix(self):
		"""True if the "reparse point fix" flag is set in this WIM's header"""
		return bool(self._wim_info.has_rpfix)

	@has_rpfix.setter
	def has_rpfix(self, value):
		try:
			self._wim_info.has_rpfix = int(value)
		except ValueError:
			raise ValueError("has_rpfix should be of type bool.")

	@property
	def image_count(self):
		"""The total number of images in this WIM file."""
		return self._wim_info.image_count

	@property
	def read_only_flag(self):
		"""True if the "readonly" flag is set in this WIM's header"""
		return bool(self._wim_info.is_marked_readonly)

	@read_only_flag.setter
	def read_only_flag(self, value):
		try:
			self._wim_info.is_marked_readonly = int(value)
		except ValueError:
			raise ValueError("hasReadOnlyFlag should be of type bool.")
	

	@property
	def is_read_only(self):
		"""
		True if this WIM file is considered readonly for any reason
		(e.g. "readonly" header flag, split WIM, filesystem permissions)
		"""
		return bool(self._wim_info.is_readonly)

	@property
	def metadata_only_flag(self):
		"""True if the "metadata only" flag is set in this WIM's header"""
		return bool(self._wim_info.metadata_only)

	@property
	def opened_from_file(self):
		""" True if this info struct is for a WIMStruct that has a backing file  """
		return bool(self._wim_info.opened_from_file)

	@property
	def part_number(self):
		""" For split WIMs, the 1-based index of this part within the split WIM; otherwise 1. """
		return self._wim_info.part_number

	@property
	def is_pipeable(self):
		"""True if this WIM file is pipable (see WIMLIB_WRITE_FLAG_PIPABLE)"""
		return bool(self._wim_info.pipable)

	@property
	def resource_only_flag(self):
		""" True if the "resource only" flag is set in this WIM's header """
		return self._wim_info.resource_only

	@property
	def is_spanned(self):
		""" True if the "spanned" flag is set in this WIM's header """
		return bool(self._wim_info.spanned)

	@property
	def total_bytes(self):
		""" The size of this WIM file in bytes, excluding the XML data and integrity table. """
		return self._wim_info.total_bytes

	@property
	def total_parts(self):
		""" For split WIMs, the total number of parts in the split WIM; otherwise 1. """
		return self._wim_info.total_parts

	@property
	def wim_version(self):
		""" The version of the WIM file format used in this WIM file. """
		return self._wim_info.wim_version

	@property
	def write_in_progress_flag(self):
		""" True if  the "write in progress" flag is set in this WIM's header. """
		return bool(self._wim_info.write_in_progress)

