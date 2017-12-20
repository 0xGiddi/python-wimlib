from wimlib import _backend, WIMError, WIMInfo, ALL_IMAGES


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


        @classmethod
        def open(cls, path, flags):
                """ Open and init WIMFile instance from file backed by disk """
                # Open and init WIMStruct
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

        def self._get_images(self):
                images = list()
                for image_index in xrange(1, self.info.image_count):
                        images.append(WIMImage(self._wim_struct, image_index))
                return images


