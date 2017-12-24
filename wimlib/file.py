import wimlib
from wimlib import _backend, WIMError
#from datetime import timedelta, datetime


class WIMFile(object):
    def __init__(self, path=None, flags=None, compression=0, callback=None, context=None):
        """ Create a new WMFile. If path is None then this is not backed by disk """
        self.path = path
        if not self.path:
            self._wim_struct = self._create_new(compression)
        else:
            if not callback:
                self._wim_struct = self._open(path, flags)
            else:
                self._wim_struct = self._open_with_progress(path, flags, callback, context)
        self.images = wimlib.image.ImageCollection(self)

    def __del__(self):
        _backend.lib.wimlib_free(self._wim_struct)

    def _open(self, path, flags):
        wim_struct = _backend.ffi.new("WIMStruct **")
        ret = _backend.lib.wimlib_open_wim(path, flags, wim_struct)
        if ret:
            raise WIMError(ret)
        return wim_struct[0]

    def _open_with_progress(self, path, flags, callback, context):
        """ Like WIMFile.Open just with a progress function, For internal use only. """
        @_backend.ffi.callback("enum wimlib_progress_status(enum wimlib_progress_msg, union wimlib_progress_info*, void*)")
        def callback_wrapper(progress_msg, progress_info, user_context):
            user_context = _backend.ffi.from_handle(user_context)
            # TODO: Cast progress_info to a pythonic object instead of C union.
            ret_val = callback(progress_msg, progress_info, user_context)
            return ret_val if ret_val is not None else 0
        context = _backend.ffi.new_handle(context)
        wim_struct = _backend.ffi.new("WIMStruct **")
        ret = _backend.lib.wimlib_open_wim_with_progress(path, flags, wim_struct, callback_wrapper, context)
        if ret:
            raise WIMError(ret)
        return wim_struct[0]

    def _create_new(self, compression):
        wim_struct = _backend.ffi.new("WIMStruct **")
        ret = _backend.lib.wimlib_create_new_wim(compression, wim_struct)
        if ret:
            raise WIMError(ret)
        return wim_struct[0]

    def write(self):
        raise NotImplementedError()

    def _write(self):
        raise NotImplementedError()

    def _overwrite(self):
        raise NotImplementedError()

    def _write_to_fd(self):
        raise NotImplementedError()

    def reference_resources(self, resource, ref_flags, wim_flags):
        """ Reference sources in other WIMs """
        # Filter resources into groups of files and wim objects
        wim_resources = list(filter(lambda res: isinstance(res, WIMFile), self.reference_resources))
        file_resources = list(filter(lambda res: isinstance(res, str), self.reference_resources))
        self._reference_resource_files(file_resources, ref_flags, wim_flags)
        self._reference_resources(wim_resources)

    def _reference_resources(self, resource_wims):
        raise NotImplementedError()

    def _reference_resource_files(self, resource_paths, ref_flags, wim_flags):
        raise NotImplementedError()

    @property
    def info(self):
        """ Get information about this WIM """
        info = _backend.ffi.new("struct wimlib_wim_info*")
        ret = _backend.lib.wimlib_get_wim_info(self._wim_struct, info)
        if ret:
            raise WIMError(ret)
        return wimlib.info.Info(info)

    @info.setter
    def info(self, value):
        if not isinstance(value, wimlib.info.Info):
            raise ValueError("Error: property info sould be set to type of Info().")
        ret = _backend.lib.wimlib_set_wim_info(self._wim_struct, value._info_struct)
        if ret:
            raise WIMError(ret)

    @property
    def xml_data(self, buffer_size=4096):
        """ Get the XML data from the file """
        out_buffer = _backend.ffi.new("void**")
        out_size = _backend.ffi.new("size_t*")
        ret = _backend.lib.wimlib_get_xml_data(self._wim_struct, out_buffer, out_size)
        if ret:
            raise WIMError(ret)
        return bytes(_backend.ffi.buffer(_backend.ffi.cast("char*", out_buffer[0]), out_size[0]))

    def extract_xml_data(self, file):
        raise NotImplementedError("Error: wimlib functions with FILE* argument not supported yet")

    def register_progress_funcion(self, callback, context):
        pass

    def verify(self, flags):
        ret = _backend.lib.wimlib_verify_wim(self._wim_struct, flags)
        if ret:
            raise WIMError(ret)

    def split(self, swm_name, part_size, flags):
        ret = _backend.lib.wimlib_split(self._wim_struct, swm_name, part_size, write_flags)
        if ret:
            raise WIMError(ret)

    def set_output_pack_compression_type(self, compression_type):
        ret = _backend.lib.wimlib_set_output_pack_compression_type(self._wim_struct, compression_type)
        if ret:
            raise WIMError(ret)

    def set_output_pack_chunk_size(self, chunk_size):
        ret = _backend.lib.wimlib_set_output_pack_chunk_size(self, chunk_size)
        if ret:
            raise WIMError(ret)

    def set_output_compression_type(self, compression_type):
        ret = _backend.lib.wimlib_set_output_compression_type(self._wim_struct, compression_type)
        if ret:
            raise WIMError(ret)

    def set_output_chunk_size(self, chunk_size):
        ret = _backend.lib.wimlib_set_output_chunk_size(self._wim_struct, chunk_size)
        if ret:
            raise WIMError(ret)

    def iterate_lookup_table(self, flags, callback, context):
        @_backend.ffi.callback("int(const struct wimlib_resource_entry, void*)")
        def callback_wrapper(resource_entry, user_context):
            user_context = _backend.ffi.from_handle(user_context)
            # TODO: Cast resource_entry to a pythonic object instead of C struct.
            ret_val = callback(resource_entry, user_context)
            return ret_val if ret_val is not None else 0
        context = _backend.ffi.new_handle(context)
        ret = _backend.lib.wimlib_iterate_lookup_table(self._wim_struct, flags, callback_wrapper, context)
        if ret:
            raise WIMError(ret)



class WIMDirEntry(object):
        def __init__(self, dentry):
                self._entry = dentry

        @property
        def filename(self):
                if self._entry.filename != _backend.ffi.NULL:
                        return _backend.ffi.string(self._entry.filename)
                return ''

        @property
        def dos_name(self):
                if self._entry.dos_name != _backend.ffi.NULL:
                        return _backend.ffi.string(self._entry.dos_name)
                return ''

        @property
        def full_path(self):
                if self._entry.full_path != _backend.ffi.NULL:
                        return _backend.ffi.string(self._entry.full_path)
                return ''

        @property
        def depth(self):
                return self._entry.depth

        @property
        def security_descriptor(self):
                raise NotImplementedError()

        @property
        def security_descriptor_size(self):
                return self._entry.security_descriptor_size

        @property
        def attributes(self):
                return self._entry.attributes

        @property
        def reparse_tag(self):
                return self._entry.reparse_tag

        @property
        def num_links(self):
                return self._entry.num_links

        @property
        def num_named_streams(self):
                return self._entry.num_named_streams

        @property
        def hard_link_group_id(self):
                return self._entry.hard_link_group_id

        @property
        def creation_time(self):
                """
                Creation time of the file.
                This will take in to account the creaion_time_high field
                """
                return datetime.fromtimestamp(self._entry.creation_time.tv_sec) + timedelta(microseconds=self._entry.creation_time.tv_nsec//1000)
        
        @property
        def last_write_time(self):
                return datetime.fromtimestamp(self._entry.last_write_time.tv_sec) + timedelta(microseconds=self._entry.last_write_time.tv_nsec//1000)
        
        
        @property
        def last_access_time(self):
                return datetime.fromtimestamp(self._entry.last_access_time.tv_sec) + timedelta(microseconds=self._entry.last_access_time.tv_nsec//1000)
        
        @property
        def unix_uid(self):
                return self._entry.unix_uid

        @property
        def unix_gid(self):
                return self._entry.unix_gid

        @property
        def object_id(self):
                return self._entry.object_id


         




