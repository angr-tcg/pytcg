#
# Build libtcg interface
#
from cffi import FFI
ffibuilder = FFI()

# FIXME: Should really be using LD_LIBRARY_PATH, but let's just hardcode it
# here for simplicity
import os
path_to_libtcg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libtcg', 'libtcg-x86_64.so.2.8.50')

ffibuilder.set_source("libtcg",
r"""
#include <dlfcn.h>
#include <assert.h>
#include <stdio.h>

#include <libtcg.h>

/* Helper startup function to load libtcg */
libtcg_init_func init_libtcg(void) {
    /* Load libtcg */
    void *handle = dlopen("%s", RTLD_LAZY);
    assert(handle != NULL);
    
    libtcg_init_func libtcg_init;
    libtcg_init = dlsym(handle, "libtcg_init");

    return libtcg_init;
}

#define TARGET_LONG_BITS 64
#define tcg_debug_assert assert

/* tcg-common.c */
#include "tcg.h"
#include "tcg-target.h"
LibTCGOpDef tcg_op_defs[] = {
#define DEF(s, oargs, iargs, cargs, flags) \
         { #s, oargs, iargs, cargs, iargs + oargs + cargs, flags },
#include "tcg-opc.h"
#undef DEF
};
    """ % path_to_libtcg,
    include_dirs=['inc', 'libtcg'],
    libraries=['dl'])

# FIXME: Should be generating the API.h file from libtcg, but CFFI C parser
# is pretty picky.
src = open('inc/api.h', 'r').read()
src += r"""
libtcg_init_func init_libtcg(void);
LibTCGOpDef tcg_op_defs[];
"""
ffibuilder.cdef(src)

if __name__ == "__main__":
   ffibuilder.compile(verbose=True)
