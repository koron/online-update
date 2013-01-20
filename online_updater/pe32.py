# -*- coding: utf-8 -*-

# EXE(PE32+)の中身が32bitか64bitか判定する.
#
# 参考: http://msdn.microsoft.com/en-us/library/ms680198(v=VS.85).aspx

import os
import struct
import sys

ARCH_ERROR = 0
ARCH_WIN32 = 1
ARCH_WIN64 = 2
ARCH_UNKNOWN = 3

def __skip(f, size):
    f.seek(size, os.SEEK_CUR)

def __read16(f):
    return struct.unpack_from('<h', f.read(2))[0]

def __read32(f):
    return struct.unpack_from('<i', f.read(4))[0]

def detectArch(path):
    f = open(path, 'rb')
    try:
        # IMAGE_NT_HEADERSまで飛ばす.
        head = f.read(2)
        if head != b'MZ':
            return ARCH_ERROR
        __skip(f, 58)
        offset = __read32(f)
        __skip(f, offset - 64)

        # IMAGE_OPTIONAL_HEADERまで飛ばす.
        head2 = f.read(2)
        if head2 != b'PE':
            return ARCH_ERROR
        __skip(f, 22)

        # IMAGE_OPTIONAL_HEADER.Magicで判定する.
        magic = __read16(f)
        if magic == 0x010B:
            return ARCH_WIN32
        elif magic == 0x020B:
            return ARCH_WIN64
        else:
            return ARCH_UNKNOWN

    finally:
        f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: %s {EXEFILE}' % sys.argv[0])
        pass
    else:
        arch = detectArch(sys.argv[1])
        print('arch=%d' % arch)
