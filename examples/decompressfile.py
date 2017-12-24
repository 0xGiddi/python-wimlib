#!/usr/bin/env python
# -*- coding: utf-8 -*-

# compressfile.py - An example of using wimlib's compression API to compress a file.
#
# This program does *not* have anything to do with WIM files other than the
# fact that this makes use of compression formats that are used in WIM files.
# This is purely an example of using the compression API.

from __future__ import print_function
import wimlib
import sys, struct, argparse

def decompress(in_fd, out_fd, chunk_size, decompressor):
    chunk_num = 0
    while True:
        in_metadata = in_fd.read(8)
        if not in_metadata:
            # No more data to compress
            break;

        u_size, c_size = struct.unpack("<ii", in_metadata)
        print("Compressed: {0}, Uncompresed {1}".format(c_size, u_size))
        if (c_size > u_size) or (u_size > chunk_size):
            raise Exception("The Data is invalid!")


        if u_size == c_size:
            in_data = in_fd.read(u_size)
            if len(in_data) != u_size:
                raise Exception("Expected to read {0} bytes of unsomoressed data".format(u_size))
        else:
            in_data = in_fd.read(c_size)
            if len(in_data) != c_size:
                raise Exception("Expected to read {0} bytes of compressed data".format(c_size))
            out_data = decompressor.decompress(in_data, u_size)

        print("Chunk {0}: {1} => {2}".format(chunk_num, c_size, u_size)) 
        out_fd.write(out_data)
        chunk_num += 1
        # All done
        # No need to free any buffers...


def main(compression_type, chunk_size, in_file, out_file):
    try:
        # Open input file
        with open(in_file, "rb") as input_file:
            # Open output file

            # read compression type and block size
            ctype, block_size = struct.unpack('<ii', input_file.read(8))

            with open(out_file, "wb") as output_file:
                # Create compressor
                decompressor = wimlib.compression.Decompressor(ctype, block_size)
    
                # Do the actual compressing
                decompress(input_file, output_file, chunk_size, decompressor)
        # No need to call wimlib_free_compressor() this will be done unpon compressor destruction.
    except Exception as ex:
        raise #print("Error: {0}".format(ex.message))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: decompressfile [LZX | XPRESS | LZMS] [chunk size] INFILE OUTFILE", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
