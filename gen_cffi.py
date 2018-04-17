#
# Build libtcg interface
#
from cffi import FFI
ffibuilder = FFI()

src = \
r"""
#include <dlfcn.h>
#include <assert.h>
#include <stdio.h>
#include <libtcg.h>
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
"""

ffibuilder.set_source("libtcg", src, include_dirs=['inc', 'libtcg'], libraries=['dl'])

# FIXME: Should be generating the API.h file from libtcg, but CFFI C parser
# is pretty picky.
src = open('inc/api.h', 'r').read()
src += r"""
LibTCGOpDef tcg_op_defs[];
"""
ffibuilder.cdef(src)

if __name__ == "__main__":
   ffibuilder.compile(verbose=True)
