#
# Build libtcg interface
#
from cffi import FFI
ffibuilder = FFI()

ffibuilder.set_source("libtcg",
   r"""
#include <dlfcn.h>
#include <assert.h>
#include <libtcg.h>
libtcg_init_func init_libtcg(void) {
/* Load libtcg */
void *handle = dlopen("../libtcg/libtcg-x86_64.so.2.8.50", RTLD_LAZY);
assert(handle != NULL);
libtcg_init_func libtcg_init;
libtcg_init = dlsym(handle, "libtcg_init");
return libtcg_init;
}

#include <stdio.h>
void sayhi(void) {
    printf("hi!\n");
}

#define TARGET_LONG_BITS 64

/* tcg-common.c */
#include "tcg.h"
#include "tcg-target.h"
LibTCGOpDef tcg_op_defs[] = {
#define DEF(s, oargs, iargs, cargs, flags) \
         { #s, oargs, iargs, cargs, iargs + oargs + cargs, flags },
#include "tcg-opc.h"
#undef DEF
};
    """,
    include_dirs=['../libtcg'],
    libraries=['dl'])

src = open('api.h', 'r', encoding='utf-8').read()
src += "\nlibtcg_init_func init_libtcg(void);"
src += "\nvoid sayhi(void);"
src += "\nLibTCGOpDef tcg_op_defs[];"
ffibuilder.cdef(src)

if __name__ == "__main__":
   ffibuilder.compile(verbose=True)
