from wimlib import _backend, WIMError

class ImageCollection(object):
    """
    This class represents a collection of images inside a WIM file.
    All funcion to do with adding/deleting/exporting images are here.
    """
    def __init__(self, wim_obj):
            self._wim_obj = wim_obj
            self.images = {}
            self.refresh()

    def __getitem__(self, key):
        try:
            return self.images[key]
        except KeyError:
            raise KeyError("Image at index {0} not found.".format(key))

    @property
    def _wim_struct(self):
        return self._wim_obj._wim_struct

    def refresh(self, return_last=False):
        """ Refresh the objects image list """
        for index in xrange(1, self._wim_obj.info.image_count + 1):
            self.images[index] = Image(index, self._wim_obj)
        if return_last:
            return self.images[max(self.images, key=int)]

    def add_empty(self, name=""):
        """ Add an empty image """
        ret = _backend.lib.wimlib_add_empty_image(self._wim_struct, name, _backend.ffi.NULL)
        if ret:
            raise WIMError(ret)
        return self.refresh(True)

    def add(self, source, name="", config="", flags=0):
        """ Add image from filesystem path """
        ret = _backend.lib.wimlib_add_image(self._wim_struct, source, name, config, flags)
        if ret:
            raise WIMError(ret)
        return self.refresh(True)

    def add_multisource():
        """ Add image from multiple filesystem paths """
        raise NotImplementedError()

    def delete(self, image):
        """ Delete an image """
        try:
            image = int(image)
        except ValueError:
            raise ValueError("Error: Argument image must be of type int() or Image()")
        ret = _backend.lib.wimlib_delete_image(self._wim_struct, image)
        if ret:
            raise WIMError(ret)

    def is_name_in_use(self, name):
        """ Check if image name is in use already (case sensitive) """
        return _backend.lib.wimlib_image_name_in_use(self._wim_struct, name)

    def resolve(self, name_or_num):
        """ Resolve a string name / number to image index (read docs for catches)"""
        ret = _backend.lib.wimlib_resolve_image(self._wim_struct, name_or_num)
        return None if not ret else ret

    # TODO: Maybe this should be an Image() method? It operates on a specific Image.
    def reference_template(self, image, template_image, template_wim=None, flags=0):
        """ Declare that a newly added image is mostly the same as a prior image. """
        if not template_wim and not isinstance(template_image, Image):
            raise ValueError("Error: template_image must be instance of Image() if no template_wim defined.")

        if isinstance(template_image, Image):
            template_wim = template_image._wim_struct

        ret = _backend.lib.wimlib_reference_template_image(self._wim_struct, image, template_wim._wim_struct, int(template_image), flags)
        if ret:
            raise WIMError(ret)


class Image(object):
    """
    This class represents an image inside a WIM file.
    All function to do with image content manupulation are here.
    """
    def __init__(self, index, wim_obj):
        self.index = index
        self._wim_obj = wim_obj
        self.mounts = []

    def __int__(self):
        """ Returns the Image.index on cast to int() """
        return self.index

    @property
    def _wim_struct(self):
        """ Get the WIMStruct for this image. For internal use. """
        return self._wim_obj._wim_struct

    @property
    def name(self):
        """ Get the name of the image """
        value = _backend.lib.wimlib_get_image_name(self._wim_struct, self.index)
        return _backend.ffi.string(value) if value else ""

    @name.setter
    def name(self, value):
        """ Set the name of the image """
        ret = _backend.lib.wimlib_set_image_name(self._wim_struct, self.index, value)
        if ret:
            raise WIMError(ret)

    @property
    def description(self):
        """ Get the description of the image """
        value = _backend.lib.wimlib_get_image_description(self._wim_struct, self.index)
        return _backend.ffi.string(value) if value else ""

    @description.setter
    def description(self, value):
        """ Set the description of the image """
        ret = _backend.lib.wimlib_set_image_descripton(self._wim_struct, self.index, value)
        if ret:
            raise WIMError(ret)

    def get_property(self, property_name):
        """ Get a property from the XML metadata for the image """
        value = _backend.lib.wimlib_get_image_property(self._wim_struct, self.index, property_name)
        return _backend.ffi.string(value) if value else ""

    def set_property(self, property_name, value):
        """ Set a property in the XML metadata for the image """
        ret = _backend.lib.wimlib_set_image_property(self._wim_struct, self.index, property_name, value)
        if ret:
            raise WIMError(ret)

    def set_flags(self, flags):
        """ Set the FLAGS property in the XML metadata. This is like Image.set_property("FLAGS", value) """
        ret = _backend.lib.wimlib_set_image_flags(self._wim_struct, self.index, flags)
        if ret:
            raise WIMError(ret)

    def mount(self, mount_dir, flags=0, staging_dir=_backend.ffi.NULL):
        """ Mount the image in the specified target directory """
        ret = _backend.lib.wimlib_mount_image(self._wim_struct, self.index, mount_dir, flags, staging_dir)
        if ret:
            raise WIMError(ret)
        self.mounts.append(mount_dir)

    def unmount(self, mount_dir, flags=0, progress_func=None, progress_context=None):
        """ Unmount the mounted image in the specified directory. """
        if not progress_func:
            ret = _backend.lib.wimlib_unmount_image(mount_dir, flags)
            if ret:
                raise WIMError(ret)
        else:
            self._unmount_with_progress(mount_dir, flags, callback, context)
        self.mounts.remove(mount_dir)

    def _unmount_with_progress(self, mount_dir, flags, callback, context=None):
        """ Like Image.unmount just with a progress function, For internal use only. """
        @_backend.ffi.callback("enum wimlib_progress_status(enum wimlib_progress_msg, union wimlib_progress_info*, void*)")
        def callback_wrapper(progress_msg, progress_info, user_context):
            user_context = _backend.ffi.from_handle(user_context)
            # TODO: Cast progress_info to a pythonic object instead of C union.
            ret_val = callback(progress_msg, progress_info, user_context)
            return ret_val if ret_val is not None else 0
        context = _backend.ffi.new_handle(context)
        ret = _backend.lib.wimlib_unmount_image_with_progress(mount_dir, flags, callback_wrapper, context)
        if ret:
            raise WIMError(ret)

    def add_tree(self, source_path, target_path, flags):
        """ Add content to the image from the local filesystem """
        ret = _backend.lib.wimlib_add_tree(self._wim_struct, self.index, source_path, target_path, flags)
        if ret:
            raise WIMError(ret)

    def rename_path(self, source_path, target_path):
        """ Rename a pah inside the image """
        ret = _backend.lib.wimlib_rename_path(self._wim_struct, self.index, source_path, target_path)
        if ret:
            raise WIMError(ret)

    def delete_path(self, path, flags):
        """ Delete a path inside the image """
        ret = _backend.lib.wimlib_delete_path(self._wim_struct, self.index, path, flags)
        if ret:
            raise WIMError(ret)

    def iterate_dir_tree(self, path, flags, callback, context=None):
        """ Iterate over the files/directories in the image """
        @_backend.ffi.callback("int(struct wimlib_dir_entry*, void*)")
        def callback_wrapper(dir_entry, user_context):
            user_context = _backend.ffi.from_handle(user_context)
            # TODO: Cast dir_entry into a more pythonic object instead of C struct.
            ret_val = callback(dir_entry, user_context)
            return ret_val if ret_val is not None else 0
        context = _backend.ffi.new_handle(context)
        ret = _backend.lib.wimlib_iterate_dir_tree(self._wim_struct, self.index, path, flags, callback_wrapper, context)
        if ret:
            raise WIMError(ret)

    def update(self, commands, flags):
        """ Execute multiple update commands on the image """
        raise NotImplementedError()

    def extract(self, target, flags):
        """ Extract the image to the specified directory or unmounted NTFS volume """
        ret = _backend.lib.wimlib_extract_image(self._wim_struct, self.index, target, flags)
        if ret:
            raise WIMError(ret)

    # TODO: Add wimlib_extract_image_from_pipe and wimlib_extract_image_from_pipe_with_progress

    def extract_paths(self, target, paths, flags):
        """ Extract a list of paths from the image """
        paths = [_backend.ffi.new("char[]", path) for path in paths]
        paths_array = _backend.ffi.new("char*[]", paths)
        ret = _backend.lib.wimlib_extract_paths(self._wim_struct, self.index, target, paths_array, len(paths), flags)
        if ret:
            raise WIMError(ret)

    def extract_pathlist(self, target, pathlist_file, flags):
        """ Like Image.extract_paths but pathlist is a file on the local filesystem"""
        ret = _backend.lib.wimlib_extract_pathlist(self._wim_struct, self.index, target, pathlist_file, flags)
        if ret:
            raise WIMError(ret)

    def export_image(self, target_wim, target_name, target_desciption, flags):
        """ Export the image to a diffrent WIM file """
        raise NotImplementedError()

