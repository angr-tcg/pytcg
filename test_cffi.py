# FFI interface to libtcg (run build_ffi first)
from libtcg import ffi, lib
import ctypes
import sys

libc_so = {"darwin": "libc.dylib", "linux": ""}[sys.platform]
libc = ctypes.CDLL(libc_so, use_errno=True, use_last_error=True)

# void* memcpy( void *dest, const void *src, size_t count );
memcpy = libc.memcpy
memcpy.restype = ctypes.c_void_p
memcpy.argtypes = (ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)

tcg = lib.init_libtcg()(b'qemu64', 0xb0000000)
assert(tcg is not None)

# Map in a page we can write to
# address = libtcg->mmap(0,
#                         4096,
#                         PROT_READ | PROT_WRITE,
#                         MAP_PRIVATE | MAP_ANONYMOUS,
#                         -1,
#                         0);
address = tcg.mmap(0, 4096, 3, 0x22, -1, 0)
# print(address.pointer)
# print(hex(address.virtual_address))

# Load in test assembly file
code = open('../libtcg_test/test_asm.bin', 'rb').read()
dest = int(ffi.cast("uintptr_t", address.pointer))
ctypes.memmove(dest, code, len(code))

# Translate block of instructions
instructions = tcg.translate(address.virtual_address)

print("global_temps:     %d" % instructions.global_temps)
print("total_temps:      %d" % instructions.total_temps)
print("virtual_addr:     0x%x" % address.virtual_address)
print("num instructions: %d" % instructions.instruction_count)

for i in range(instructions.instruction_count):
    op = instructions.instructions[i]
    op_def = lib.tcg_op_defs[op.opc]
    name = ffi.string(op_def.name)
    # print('TCG %s %d %d %d' % (name, op_def.nb_oargs, op_def.nb_iargs, op_def.nb_cargs))
    lib.tcg_dump_ops(
        ffi.addressof(instructions),
        ffi.addressof(op),
        ffi.addressof(op_def),
        op.args
        )

tcg.free_instructions(ffi.addressof(instructions))
