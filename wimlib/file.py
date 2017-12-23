from wimlib import _backend, WIMError, WIMInfo, ALL_IMAGES
from wimlib.observer import Observerable, notify_observers
from datetime import timedelta, datetime

def refresh(attribute):
        def _refresh(func):
                def wrapper(self, *args):
                        retval = func(self, *args)
                        self._refresh()
                        return retval
                return wrapper
        return _refresh


class UpdateCommand(object):
        pass

class WIMFile(object):
        """
        WIMFile represents a single WIM file.
        The WIM file can be either opened and init
        from a file backed by disk or created from scratch
        in memory
        """
        def __init__(self, wim_struct, path=None):
                """ WIMFile C'tor, use WIMFile.open or WIMFile.create """
                self.path = path
                self._wim_struct = wim_struct
                self.info = WIMInfo(self._wim_struct)
                if not path:
                        self._is_new = True
                else:
                        self._is_new = False

                self.images = self._get_images()

        def _refresh(self):
                self.info._refresh()
                self.images = self._get_images()
                for image in self.images.values():
                        image._refresh()


        @classmethod
        def open(cls, path, flags, progress_callback=None, progress_context=None):
                """ Open and init WIMFile instance from file backed by disk """
                #@_backend.ffi.callback("int(struct wimlib_dir_entry*, void*)")
                #def callback_wrapper(dir_entry, context):
                #        context = _backend.ffi.from_handle(context)
                #        return_val = callback(dir_entry, context)
                #        return return_val if return_val is not None else 0
                if progress_callback:
                        @_backend.ffi.callback("int(int,union wimlib_progress_info *,void*)")
                        def progress_callback_wrapper(msg_type, info, context):
                                context = _backend.ffi.from_handle(context)
                                ret_val = progress_callback(msg_type, info, context)
                                return ret_val if ret_val else 0

                wstruct = _backend.ffi.new("WIMStruct **")
                ret = _backend.lib.wimlib_open_wim(path, flags, wstruct)
                if ret:
                        raise WIMError(ret)

                if ret:
                        raise WIMError(ret)
                return cls(wstruct[0], path)

        @classmethod
        def create(cls, compression_type):
                """ Create a new WIM file """
                wstruct = _backend.ffi.new("WIMStruct **")
                ret = _backend.lib.wimlib_create_new_wim(compression_type, wstruct)
                if ret:
                        raise WIMError(ret)
                
                return cls(wstruct[0])

        def _overwrite(self, flags=0, threads=1):
                ret = _backend.lib.wimlib_overwrite(self._wim_struct, flags, threads)
                if ret:
                        raise WIMError(ret)

        def _write(self, path, image=ALL_IMAGES, flags=0, threads=1):
                ret = _backend.lib.wimlib_write(self._wim_struct, path, image, flags, threads)
                if ret:
                        raise WIMError(ret)

        def write(self, **kwargs):
                """
                Write the wim sruct and images to a file.
                
                Params:
                If the wim file was created:
                        path - location to save, defaults to last location written
                        image - list of images to write (defaults to all)
                        flags - defaults to 0
                        threads - defaults to 1
                If the file was opened:
                        flags - defaults to 0
                        thread - defaults to 1
                """

                path = kwargs.get("path") if "path" in kwargs else self.path
                image = kwargs.get("image") if "image" in kwargs else ALL_IMAGES
                flags = kwargs.get("flags") if "flags" in kwargs else 0
                threads = kwargs.get("threads") if "threads" in kwargs else 0

                if self._is_new:
                        if not path:
                                raise Exception("Path must be specified on first write of new WIM")
                        self._write(path, image, flags, threads)
                        self.path = path
                else:
                        self._overwrite(flags, threads)

        def write_to_fd(self):
                raise NotImplementedError()

        def set_output_chunk_size(self, size):
                """ 
                Set a WIMStruct's output compression chunk size.

                This is the compression chunk size that will be used for writing non-solid 
                resources in subsequent calls to write(). A larger 
                compression chunk size often results in a better compression ratio, but 
                compression may be slower and the speed of random access to data may be reduced. 
                In addition, some chunk sizes are not compatible with Microsoft software. 
                """
                ret = _backend.lib.wimlib_set_output_chunk_size(self._wim_struct, size)
                if ret:
                        raise WIMError(ret)

        def set_output_pack_chunk_size(self, size):
                ret = _backend.lib.wimlib_set_output_pack_chunk_size(self._wim_struct, size)
                if ret:
                        raise WIMError(ret)

        def set_output_compression_type(self, ctype):
                ret = _backend.lib.wimlib_set_output_compression_type(self._wim_struct, ctype)
                if ret:
                        raise WIMError(ret)

        def set_output_pack_compression_type(self, ctype):
                ret = _backend.lib.wimlib_set_output_pack_compression_type(self._wim_struct, ctype)
                if ret:
                        raise WIMError(ret)

        def _get_images(self):
                images = dict()
                for image_index in xrange(1, (self.info.image_count+1)):
                        images[image_index] = WIMImage(self, image_index)
                return images

        def get_xml(self):
                pass


        def add_empty_image(self, name=None):
                """ Adds an empty image to the WIMFile and returns the new image """
                ret = _backend.lib.wimlib_add_empty_image(self._wim_struct, name, _backend.ffi.NULL)
                if ret:
                        raise WIMError(ret)
                self._refresh()
                return self.images[max(self.images, key=int)]


        def add_image(self, source_path, name=None, flags=None, config_file=None):
                """ A a image from path or volume """
                ret = _backend.lib.wimlib_add_image(self._wim_struct, source_path, name, config_file, flags)
                if ret:
                        raise WIMError(ret)
                self._refresh()
                return self.images[max(self.images, key=int)]


        def add_image_multisource(self, sources, name, config_file, flags):
                ret = _backend.lib.wimlib_add_image_multisource(self._wim_struct, sources, len(sources), name, config_file, flags)
                if ret:
                        raise WIMError(ret)
                self._refresh()
                return self.images[max(self.images, key=int)]





class WIMImage(object):
        def __init__(self, wim, index=0):
                super(WIMImage, self).__init__()
                self._wim_struct = wim._wim_struct if type(wim) is WIMFile else wim
                self.index = index

                # If we have a index this is not a new image
                if self.index:
                        pass

        def _refresh(self):
                pass

        def get_property(self, property_name):
                value = _backend.lib.wimlib_get_image_property(self._wim_struct, self.index, property_name)
                if value == _backend.ffi.NULL:
                        return None
                return value

        def set_property(self, property_name, value):
                ret = _backend.lib.wimlib_set_propery_name(self._wim_struct, self.index, property_name, value)
                if ret:
                        raise WIMError(ret)

        @property
        def name(self):
                value = _backend.lib.wimlib_get_image_name(self._wim_struct, self.index) 
                if value == _backend.ffi.NULL:
                        return None
                return value

        @name.setter
        def name(self, name):
                ret = _backend.lib.wimlib_set_image_name(self._wim_struct, self.index, name)
                if ret:
                        raise WIMError(ret)

        @property
        def description(self):
                value = _backend.lib.wimlib_get_image_description(self._wim_struct, self.index) 
                if value == _backend.ffi.NULL:
                        return None
                return value

        @description.setter
        def description(self, descripion):
                ret = _backend.lib.wimlib_set_image_descripion(self._wim_struct, self.index, descripion)
                if ret:
                        raise WIMError(ret)


        def rename_path(self, source_path, dest_path):
                ret = _backend.lib.wimlib_rename_path(self._wim_struct, self.index, source_path, dest_path)
                if ret:
                        raise WIMError(ret)

        def delete_path(self, path, flags):
                ret = wimlib_delete_path(self._wim_struct, self.index, path, flags)
                if ret:
                        raise WIMError(ret)

        
        def add_tree(self, source, target, flags):
                ret = _backend.lib.wimlib_add_tree(self._wim_struct, self.index, source, target, flags)
                if ret:
                        raise WIMError(ret)

        def export(self, dest_wim, dest_name=None, dest_desciption=None, flags=None):
                dest_wim = dest_wim._wim_struct if type(dest_wim) is WIMFile else dest_wim
                ret = _backend.lib.wimlib_export_image(self._wim_struct, self.index, dest_wim, dest_name, dest_desciption, flags)
                if ret:
                        raise WIMError(ret)

        def update(self, commands, flags):
                """ Update an image using commands """
                cmds = [command._raw_object for command in commands]
                ret = _backend.lib.wimlib_update_image(self._wim_struct, self.index, cmds, len(cmds), flags)
                if ret:
                        raise WIMError(ret)

        def set_flags(self, flags):
                ret = _backend.lib._wimlib_set_image_flags(self._wim_struct, self.index, flags)
                if ret:
                        raise WIMError(ret)

        def iter_tree(self, path, flags, callback, callback_params=None):
                @_backend.ffi.callback("int(struct wimlib_dir_entry*, void*)")
                def callback_wrapper(dir_entry, context):
                        context = _backend.ffi.from_handle(context)
                        return_val = callback(dir_entry, context)
                        return return_val if return_val is not None else 0

                cb_params = _backend.ffi.new_handle(callback_params)
                ret = _backend.lib.wimlib_iterate_dir_tree(self._wim_struct, self.index, path, flags, callback_wrapper, cb_params)
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


         




