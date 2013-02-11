from macholib.ptypes import p_uint32

# Taken from /usr/include/mach-o/loader.h (on 10.7). We only load
ID_TO_COMMAND_NAME = {
        p_uint32(0xd): "LC_ID_DYLIB",
        p_uint32(0xe): "LC_LOAD_DYLINKER",
}

COMMAND_NAME_TO_ID = dict((v, k) for k, v in ID_TO_COMMAND_NAME.iteritems())
