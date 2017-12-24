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

def compress(in_fd, out_fd, chunk_size, compressor):
    chunk_num = 0
    while True:
        in_data = in_fd.read(chunk_size)
        in_size = len(in_data)

        if not in_data:
            # No more data to compress
            break;

        out_size, out_data = compressor.compress(in_data)
        if not out_size:
            out_data = in_data
            out_size = in_size

        print("Chunk {0}: {1} => {2}".format(chunk_num, in_size, out_size))
        out_fd.write(struct.pack("<i", in_size))
        out_fd.write(struct.pack("<i", out_size))
        out_fd.write(out_data)
        chunk_num += 1

        # All done
        # No need to free any buffers...


def main(compression_type, chunk_size, in_file, out_file):
    ctype = None

    # Parse compression type
    for i in range(1, 4):
        if wimlib.compression.get_compression_type_string(i) == compression_type:
            ctype = i
            break

    if not ctype:
        print("Unrecognized compression type '{0}'", compression_type, file=sys.stderr)
        return 1

    # Parse chunk size
    try:
        chunk_size = int(chunk_size)
    except ValueError:
        print("Bad chunk size '{0}'", chunk_size, file=sys.stderr)
        return 2

    try:
        # Open input file
        with open(in_file, "rb") as input_file:
            # Open output file
            with open(out_file, "wb") as output_file:
                # Create compressor
                compressor = wimlib.compression.Compressor(ctype, chunk_size)
    
                # Write compression type and chunk size to output file
                output_file.write(struct.pack('<i', ctype))
                output_file.write(struct.pack('<i', chunk_size))
    
                # Do the actual compressing
                compress(input_file, output_file, chunk_size, compressor)
        # No need to call wimlib_free_compressor() this will be done unpon compressor destruction.
    except Exception as ex:
        print("Error: {0}".format(ex.message))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: compressfile [LZX | XPRESS | LZMS] [chunk size] INFILE OUTFILE", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
