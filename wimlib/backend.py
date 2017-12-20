import cffi
import platform


# C wimlib defenitions
# All function, unions and structs are as defined in wimlib.h
# enums are defined only with a max value for silencing cffi warnings.
# TODO: Replace base64 with proper multiline string, this is only for testing while developing.
WIMLIB_DEFAULT_CDEFS = """
typedef char wimlib_tchar;
struct wimlib_timespec {
        int64_t tv_sec;
        int32_t tv_nsec;
};

typedef struct WIMStruct WIMStruct;

union wimlib_progress_info {
        struct wimlib_progress_info_write_streams {
                uint64_t total_bytes;
                uint64_t total_streams;
                uint64_t completed_bytes;
                uint64_t completed_streams;
                uint32_t num_threads;
                int32_t compression_type;
                uint32_t total_parts;
                uint32_t completed_parts;
        } write_streams;
        struct wimlib_progress_info_scan {
                const wimlib_tchar *source;
                const wimlib_tchar *cur_path;
                enum {
                        WIMLIB_SCAN_DENTRY_OK = 0,
                        WIMLIB_SCAN_DENTRY_EXCLUDED = 1,
                        WIMLIB_SCAN_DENTRY_UNSUPPORTED = 2,
                        WIMLIB_SCAN_DENTRY_FIXED_SYMLINK = 3,
                        WIMLIB_SCAN_DENTRY_NOT_FIXED_SYMLINK = 4,
                } status;
                union {
                        const wimlib_tchar *wim_target_path;
                        const wimlib_tchar *symlink_target;
                };
                uint64_t num_dirs_scanned;
                uint64_t num_nondirs_scanned;
                uint64_t num_bytes_scanned;
        } scan;
        struct wimlib_progress_info_extract {
                uint32_t image;
                uint32_t extract_flags;
                const wimlib_tchar *wimfile_name;
                const wimlib_tchar *image_name;
                const wimlib_tchar *target;
                const wimlib_tchar *reserved;
                uint64_t total_bytes;
                uint64_t completed_bytes;
                uint64_t total_streams;
                uint64_t completed_streams;
                uint32_t part_number;
                uint32_t total_parts;
                uint8_t guid[16];
                uint64_t current_file_count;
                uint64_t end_file_count;
        } extract;
        struct wimlib_progress_info_rename {
                const wimlib_tchar *from;
                const wimlib_tchar *to;
        } rename;
        struct wimlib_progress_info_update {
                const struct wimlib_update_command *command;
                size_t completed_commands;
                size_t total_commands;
        } update;
        struct wimlib_progress_info_integrity {
                uint64_t total_bytes;
                uint64_t completed_bytes;
                uint32_t total_chunks;
                uint32_t completed_chunks;
                uint32_t chunk_size;
                const wimlib_tchar *filename;
        } integrity;
        struct wimlib_progress_info_split {
                uint64_t total_bytes;
                uint64_t completed_bytes;
                unsigned cur_part_number;
                unsigned total_parts;
    wimlib_tchar *part_name;
        } split;
        struct wimlib_progress_info_replace {
                const wimlib_tchar *path_in_wim;
        } replace;
        struct wimlib_progress_info_wimboot_exclude {
                const wimlib_tchar *path_in_wim;
                const wimlib_tchar *extraction_path;
        } wimboot_exclude;
        struct wimlib_progress_info_unmount {
                const wimlib_tchar *mountpoint;
                const wimlib_tchar *mounted_wim;
                uint32_t mounted_image;
                uint32_t mount_flags;
                uint32_t unmount_flags;
        } unmount;
        struct wimlib_progress_info_done_with_file {
                const wimlib_tchar *path_to_file;
        } done_with_file;
        struct wimlib_progress_info_verify_image {
                const wimlib_tchar *wimfile;
                uint32_t total_images;
                uint32_t current_image;
        } verify_image;
        struct wimlib_progress_info_verify_streams {
                const wimlib_tchar *wimfile;
                uint64_t total_streams;
                uint64_t total_bytes;
                uint64_t completed_streams;
                uint64_t completed_bytes;
        } verify_streams;
        struct wimlib_progress_info_test_file_exclusion {
                const wimlib_tchar *path;
                bool will_exclude;
        } test_file_exclusion;
        struct wimlib_progress_info_handle_error {
                const wimlib_tchar *path;
                int error_code;
                bool will_ignore;
        } handle_error;
};

struct wimlib_capture_source {
        wimlib_tchar *fs_source_path;
        wimlib_tchar *wim_target_path;
        long reserved;
};

struct wimlib_wim_info {
        uint8_t guid[16];
        uint32_t image_count;
        uint32_t boot_index;
        uint32_t wim_version;
        uint32_t chunk_size;
        uint16_t part_number;
        uint16_t total_parts;
        int32_t compression_type;
        uint64_t total_bytes;
        uint32_t has_integrity_table : 1;
        uint32_t opened_from_file : 1;
        uint32_t is_readonly : 1;
        uint32_t has_rpfix : 1;
        uint32_t is_marked_readonly : 1;
        uint32_t spanned : 1;
        uint32_t write_in_progress : 1;
        uint32_t metadata_only : 1;
        uint32_t resource_only : 1;
        uint32_t pipable : 1;
        uint32_t reserved_flags : 22;
        uint32_t reserved[9];
};

struct wimlib_resource_entry {
        uint64_t uncompressed_size;
        uint64_t compressed_size;
        uint64_t offset;
        uint8_t sha1_hash[20];
        uint32_t part_number;
        uint32_t reference_count;
        uint32_t is_compressed : 1;
        uint32_t is_metadata : 1;
        uint32_t is_free : 1;
        uint32_t is_spanned : 1;
        uint32_t is_missing : 1;
        uint32_t packed : 1;
        uint32_t reserved_flags : 26;
        uint64_t raw_resource_offset_in_wim;
        uint64_t raw_resource_compressed_size;
        uint64_t raw_resource_uncompressed_size;
        uint64_t reserved[1];
};

struct wimlib_stream_entry {
        const wimlib_tchar *stream_name;
        struct wimlib_resource_entry resource;
        uint64_t reserved[4];
};

struct wimlib_object_id {
        uint8_t object_id[16];
        uint8_t birth_volume_id[16];
        uint8_t birth_object_id[16];
        uint8_t domain_id[16];
};

struct wimlib_dir_entry {
        const wimlib_tchar *filename;
        const wimlib_tchar *dos_name;
        const wimlib_tchar *full_path;
        size_t depth;
        const char *security_descriptor;
        size_t security_descriptor_size;
        uint32_t attributes;
        uint32_t reparse_tag;
        uint32_t num_links;
        uint32_t num_named_streams;
        uint64_t hard_link_group_id;
        struct wimlib_timespec creation_time;
        struct wimlib_timespec last_write_time;
        struct wimlib_timespec last_access_time;
        uint32_t unix_uid;
        uint32_t unix_gid;
        uint32_t unix_mode;
        uint32_t unix_rdev;
        struct wimlib_object_id object_id;
        int32_t creation_time_high;
        int32_t last_write_time_high;
        int32_t last_access_time_high;
        int32_t reserved2;
        uint64_t reserved[4];
        struct wimlib_stream_entry streams[];
};

struct wimlib_add_command {
        wimlib_tchar *fs_source_path;
        wimlib_tchar *wim_target_path;
        wimlib_tchar *config_file;
        int add_flags;
};

struct wimlib_delete_command {
        wimlib_tchar *wim_path;
        int delete_flags;
};

struct wimlib_rename_command {
        wimlib_tchar *wim_source_path;
        wimlib_tchar *wim_target_path;
        int rename_flags;
};

struct wimlib_update_command {
        enum wimlib_update_op op;
        union {
                struct wimlib_add_command add;
                struct wimlib_delete_command delete;
                struct wimlib_rename_command rename;
        };
};

//Callback signature defeniions
typedef int (*wimlib_iterate_dir_tree_callback_t)(const struct wimlib_dir_entry *dentry, void *user_ctx);
typedef int (*wimlib_iterate_lookup_table_callback_t)(const struct wimlib_resource_entry *resource, void *user_ctx);
typedef enum wimlib_progress_status (*wimlib_progress_func_t)(enum wimlib_progress_msg msg_type, union wimlib_progress_info *info, void *progctx);

// Funcion signatures
int wimlib_add_empty_image(WIMStruct *wim, const wimlib_tchar *name, int *new_idx_ret);
int wimlib_add_image(WIMStruct *wim, const wimlib_tchar *source, const wimlib_tchar *name, const wimlib_tchar *config_file, int add_flags);
int wimlib_add_image_multisource(WIMStruct *wim, const struct wimlib_capture_source *sources, size_t num_sources, const wimlib_tchar *name, const wimlib_tchar *config_file, int add_flags);
int wimlib_add_tree(WIMStruct *wim, int image, const wimlib_tchar *fs_source_path, const wimlib_tchar *wim_target_path, int add_flags);
int wimlib_create_new_wim(enum wimlib_compression_type ctype, WIMStruct **wim_ret);
int wimlib_delete_image(WIMStruct *wim, int image);
int wimlib_delete_path(WIMStruct *wim, int image, const wimlib_tchar *path, int delete_flags);
int wimlib_export_image(WIMStruct *src_wim, int src_image, WIMStruct *dest_wim, const wimlib_tchar *dest_name, const wimlib_tchar *dest_description, int export_flags);
int wimlib_extract_image(WIMStruct *wim, int image, const wimlib_tchar *target, int extract_flags);
int wimlib_extract_image_from_pipe(int pipe_fd, const wimlib_tchar *image_num_or_name, const wimlib_tchar *target, int extract_flags);
//int wimlib_extract_image_from_pipe_with_progress(int pipe_fd, const wimlib_tchar *image_num_or_name, const wimlib_tchar *target, int extract_flags, wimlib_progress_func_t progfunc, void *progctx);
int wimlib_extract_pathlist(WIMStruct *wim, int image, const wimlib_tchar *target, const wimlib_tchar *path_list_file, int extract_flags);
int wimlib_extract_paths(WIMStruct *wim, int image, const wimlib_tchar *target, const wimlib_tchar * const *paths, size_t num_paths, int extract_flags);
int wimlib_extract_xml_data(WIMStruct *wim, FILE *fp);
void wimlib_free(WIMStruct *wim);
const wimlib_tchar * wimlib_get_compression_type_string(enum wimlib_compression_type ctype);
const wimlib_tchar * wimlib_get_error_string(enum wimlib_error_code code);
const wimlib_tchar * wimlib_get_image_description(const WIMStruct *wim, int image);
const wimlib_tchar * wimlib_get_image_name(const WIMStruct *wim, int image);
const wimlib_tchar * wimlib_get_image_property(const WIMStruct *wim, int image, const wimlib_tchar *property_name);
uint32_t wimlib_get_version(void);
int wimlib_get_wim_info(WIMStruct *wim, struct wimlib_wim_info *info);
int wimlib_get_xml_data(WIMStruct *wim, void **buf_ret, size_t *bufsize_ret);
int wimlib_global_init(int init_flags);
void wimlib_global_cleanup(void);
bool wimlib_image_name_in_use(const WIMStruct *wim, const wimlib_tchar *name);
int wimlib_iterate_dir_tree(WIMStruct *wim, int image, const wimlib_tchar *path, int flags, wimlib_iterate_dir_tree_callback_t cb, void *user_ctx);
int wimlib_iterate_lookup_table(WIMStruct *wim, int flags, wimlib_iterate_lookup_table_callback_t cb, void *user_ctx);
int wimlib_join(const wimlib_tchar * const *swms, unsigned num_swms, const wimlib_tchar *output_path, int swm_open_flags, int wim_write_flags);
int wimlib_join_with_progress(const wimlib_tchar * const *swms, unsigned num_swms, const wimlib_tchar *output_path, int swm_open_flags, int wim_write_flags, wimlib_progress_func_t progfunc, void *progctx);
int wimlib_mount_image(WIMStruct *wim, int image, const wimlib_tchar *dir, int mount_flags, const wimlib_tchar *staging_dir);
int wimlib_open_wim(const wimlib_tchar *wim_file, int open_flags, WIMStruct **wim_ret);
int wimlib_open_wim_with_progress(const wimlib_tchar *wim_file, int open_flags, WIMStruct **wim_ret, wimlib_progress_func_t progfunc, void *progctx);
int wimlib_overwrite(WIMStruct *wim, int write_flags, unsigned num_threads);
void wimlib_print_available_images(const WIMStruct *wim, int image);
void wimlib_print_header(const WIMStruct *wim);
int wimlib_reference_resource_files(WIMStruct *wim, const wimlib_tchar * const *resource_wimfiles_or_globs, unsigned count, int ref_flags, int open_flags);
int wimlib_reference_resources(WIMStruct *wim, WIMStruct **resource_wims, unsigned num_resource_wims, int ref_flags);
int wimlib_reference_template_image(WIMStruct *wim, int new_image, WIMStruct *template_wim, int template_image, int flags);
void wimlib_register_progress_function(WIMStruct *wim, wimlib_progress_func_t progfunc, void *progctx);
int wimlib_rename_path(WIMStruct *wim, int image, const wimlib_tchar *source_path, const wimlib_tchar *dest_path);
int wimlib_resolve_image(WIMStruct *wim, const wimlib_tchar *image_name_or_num);
int wimlib_set_error_file(FILE *fp);
int wimlib_set_error_file_by_name(const wimlib_tchar *path);
int wimlib_set_image_descripton(WIMStruct *wim, int image, const wimlib_tchar *description);
int wimlib_set_image_flags(WIMStruct *wim, int image, const wimlib_tchar *flags);
int wimlib_set_image_name(WIMStruct *wim, int image, const wimlib_tchar *name);
int wimlib_set_image_property(WIMStruct *wim, int image, const wimlib_tchar *property_name, const wimlib_tchar *property_value);
int wimlib_set_memory_allocator(void *(*malloc_func)(size_t), void (*free_func)(void *), void *(*realloc_func)(void *, size_t));
int wimlib_set_output_chunk_size(WIMStruct *wim, uint32_t chunk_size);
int wimlib_set_output_pack_chunk_size(WIMStruct *wim, uint32_t chunk_size);
int wimlib_set_output_compression_type(WIMStruct *wim, enum wimlib_compression_type ctype);
int wimlib_set_output_pack_compression_type(WIMStruct *wim, enum wimlib_compression_type ctype);
int wimlib_set_print_errors(bool show_messages);
int wimlib_set_wim_info(WIMStruct *wim, const struct wimlib_wim_info *info, int which);
int wimlib_split(WIMStruct *wim, const wimlib_tchar *swm_name, uint64_t part_size, int write_flags);
int wimlib_verify_wim(WIMStruct *wim, int verify_flags);
int wimlib_unmount_image(const wimlib_tchar *dir, int unmount_flags);
int wimlib_unmount_image_with_progress(const wimlib_tchar *dir, int unmount_flags, wimlib_progress_func_t progfunc, void *progctx);
int wimlib_update_image(WIMStruct *wim, int image, const struct wimlib_update_command *cmds, size_t num_cmds, int update_flags);
int wimlib_write(WIMStruct *wim, const wimlib_tchar *path, int image, int write_flags, unsigned num_threads);
int wimlib_write_to_fd(WIMStruct *wim, int fd, int image, int write_flags, unsigned num_threads);
int wimlib_set_default_compression_level(int ctype, unsigned int compression_level);
uint64_t wimlib_get_compressor_needed_memory(enum wimlib_compression_type ctype, size_t max_block_size, unsigned int compression_level);
int wimlib_create_compressor(enum wimlib_compression_type ctype, size_t max_block_size, unsigned int compression_level, struct wimlib_compressor **compressor_ret);
size_t wimlib_compress(const void *uncompressed_data, size_t uncompressed_size, void *compressed_data, size_t compressed_size_avail, struct wimlib_compressor *compressor);
void wimlib_free_compressor(struct wimlib_compressor *compressor);
int wimlib_create_decompressor(enum wimlib_compression_type ctype, size_t max_block_size, struct wimlib_decompressor **decompressor_ret);
int wimlib_decompress(const void *compressed_data, size_t compressed_size, void *uncompressed_data, size_t uncompressed_size, struct wimlib_decompressor *decompressor);
void wimlib_free_decompressor(struct wimlib_decompressor *decompressor);
"""

class WIMBackend(object):
        """
        WIMBackend

        This class creates the ffi and lib objects used by other wimlib
        classes. This class is for internal use only.
        """

        def __init__(self):
                self.os_family = platform.system()
                self.ffi = cffi.FFI()
                # Add OS specific C wimlib declarations
                # for Windows and Linux wimlib_tchar defenition
                self.ffi.cdef(self._get_platform_cdefs())
                # Add default C wimlib declarations
                self.ffi.cdef(WIMLIB_DEFAULT_CDEFS)
                self.lib = self.ffi.dlopen(self._get_wimlib_path())
                self.encoding = self._get_platform_encoding()

        def _get_platform_encoding(self):
                if self.os_family == "Windows":
                        return "utf-16-le"
                return "utf-8"

        def _get_platform_cdefs(self):
                if self.os_family == "Windows":
                        # wimlib_tchar is a 'wchar' on windows
                        return "typedef wchar_t wimlib_tchar;"
                # on any other platforms is a 'char'
                return "typedef char wimlib_tchar;"

        def _get_wimlib_path(self):
                if self.os_family == "Linux":
                        return "/usr/lib/libwim.so"
                elif self.os_family == "Darwin":
                        pass
                elif self.os_family == "Windows":
                        pass

                raise NotImplementedError("The current platform is not supported ({0}, {1}).".format(self.os_family, platform.architecture()))
