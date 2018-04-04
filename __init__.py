# FFI interface to libtcg (run build_ffi first)
from libtcg import ffi, lib
import ctypes
import sys

libc_so = {"darwin": "libc.dylib", "linux": ""}[sys.platform]
libc = ctypes.CDLL(libc_so, use_errno=True, use_last_error=True)

tcg = lib.init_libtcg()(b'qemu64', 0xb0000000)
assert(tcg is not None)

def main():
    # Map in a page we can write to
    address = tcg.mmap(0,
                       4096,
                       3, # PROT_READ | PROT_WRITE,
                       0x22, # MAP_PRIVATE | MAP_ANONYMOUS,
                       -1,
                       0)

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
    print('')

    for i in range(instructions.instruction_count):
        op = instructions.instructions[i]
        op_def = lib.tcg_op_defs[op.opc]
        name = ffi.string(op_def.name)
        # sys.stdout.write(' c:')
        # sys.stdout.flush()
        # lib.tcg_dump_ops(
        #     ffi.addressof(instructions),
        #     ffi.addressof(op),
        #     ffi.addressof(op_def),
        #     op.args
        #     )
        tcg_dump_ops(instructions, op, op_def, op.args)

    tcg.free_instructions(ffi.addressof(instructions))

def tcg_get_arg_str_idx(s, idx):
    assert(idx >= 0 and idx < s.total_temps)
    temp = s.temps[idx]

    if idx < s.global_temps:
        return ffi.string(temp.name).decode('utf-8')
    elif temp.temp_local:
        return 'loc%d' % (idx - s.global_temps)
    else:
        return 'tmp%d' % (idx - s.global_temps)


# /* Find helper name.  */
def tcg_find_helper(s, val):
    hinfo = tcg.find_helper(val)
    if hinfo:
        return ffi.string(hinfo.name).decode('utf-8')
    return '(unknown)'

# /**
#  * arg_label
#  * @i: value
#  *
#  * The opposite of label_arg.  Retrieve a label from the
#  * encoding of the TCG opcode stream.
#  */
def arg_label(i):
    return ffi.cast('TCGLabel *', i)

# typedef enum {
LIBTCG_COND_NEVER  = 0 | 0 | 0 | 0
LIBTCG_COND_ALWAYS = 0 | 0 | 0 | 1
LIBTCG_COND_EQ     = 8 | 0 | 0 | 0
LIBTCG_COND_NE     = 8 | 0 | 0 | 1
LIBTCG_COND_LT     = 0 | 0 | 2 | 0
LIBTCG_COND_GE     = 0 | 0 | 2 | 1
LIBTCG_COND_LE     = 8 | 0 | 2 | 0
LIBTCG_COND_GT     = 8 | 0 | 2 | 1
LIBTCG_COND_LTU    = 0 | 4 | 0 | 0
LIBTCG_COND_GEU    = 0 | 4 | 0 | 1
LIBTCG_COND_LEU    = 8 | 4 | 0 | 0
LIBTCG_COND_GTU    = 8 | 4 | 0 | 1
# } LibTCGCond;

cond_name = {
    LIBTCG_COND_NEVER:  "never",
    LIBTCG_COND_ALWAYS: "always",
    LIBTCG_COND_EQ:     "eq",
    LIBTCG_COND_NE:     "ne",
    LIBTCG_COND_LT:     "lt",
    LIBTCG_COND_GE:     "ge",
    LIBTCG_COND_LE:     "le",
    LIBTCG_COND_GT:     "gt",
    LIBTCG_COND_LTU:    "ltu",
    LIBTCG_COND_GEU:    "geu",
    LIBTCG_COND_LEU:    "leu",
    LIBTCG_COND_GTU:    "gtu",
}

# typedef enum LibTCGMemOp {
LIBTCG_MO_8        = 0
LIBTCG_MO_16       = 1
LIBTCG_MO_32       = 2
LIBTCG_MO_64       = 3
LIBTCG_MO_SIZE     = 3
LIBTCG_MO_SIGN     = 4
LIBTCG_MO_BSWAP    = 8
LIBTCG_MO_LE       = 0
LIBTCG_MO_BE       = LIBTCG_MO_BSWAP
LIBTCG_MO_TE       = LIBTCG_MO_LE
LIBTCG_MO_ASHIFT   = 4
LIBTCG_MO_AMASK    = 7 << LIBTCG_MO_ASHIFT
LIBTCG_MO_ALIGN    = LIBTCG_MO_AMASK
LIBTCG_MO_UNALN    = 0
LIBTCG_MO_ALIGN_2  = 1 << LIBTCG_MO_ASHIFT
LIBTCG_MO_ALIGN_4  = 2 << LIBTCG_MO_ASHIFT
LIBTCG_MO_ALIGN_8  = 3 << LIBTCG_MO_ASHIFT
LIBTCG_MO_ALIGN_16 = 4 << LIBTCG_MO_ASHIFT
LIBTCG_MO_ALIGN_32 = 5 << LIBTCG_MO_ASHIFT
LIBTCG_MO_ALIGN_64 = 6 << LIBTCG_MO_ASHIFT
LIBTCG_MO_UB       = LIBTCG_MO_8
LIBTCG_MO_UW       = LIBTCG_MO_16
LIBTCG_MO_UL       = LIBTCG_MO_32
LIBTCG_MO_SB       = LIBTCG_MO_SIGN | LIBTCG_MO_8
LIBTCG_MO_SW       = LIBTCG_MO_SIGN | LIBTCG_MO_16
LIBTCG_MO_SL       = LIBTCG_MO_SIGN | LIBTCG_MO_32
LIBTCG_MO_Q        = LIBTCG_MO_64
LIBTCG_MO_LEUW     = LIBTCG_MO_LE | LIBTCG_MO_UW
LIBTCG_MO_LEUL     = LIBTCG_MO_LE | LIBTCG_MO_UL
LIBTCG_MO_LESW     = LIBTCG_MO_LE | LIBTCG_MO_SW
LIBTCG_MO_LESL     = LIBTCG_MO_LE | LIBTCG_MO_SL
LIBTCG_MO_LEQ      = LIBTCG_MO_LE | LIBTCG_MO_Q
LIBTCG_MO_BEUW     = LIBTCG_MO_BE | LIBTCG_MO_UW
LIBTCG_MO_BEUL     = LIBTCG_MO_BE | LIBTCG_MO_UL
LIBTCG_MO_BESW     = LIBTCG_MO_BE | LIBTCG_MO_SW
LIBTCG_MO_BESL     = LIBTCG_MO_BE | LIBTCG_MO_SL
LIBTCG_MO_BEQ      = LIBTCG_MO_BE | LIBTCG_MO_Q
LIBTCG_MO_TEUW     = LIBTCG_MO_TE | LIBTCG_MO_UW
LIBTCG_MO_TEUL     = LIBTCG_MO_TE | LIBTCG_MO_UL
LIBTCG_MO_TESW     = LIBTCG_MO_TE | LIBTCG_MO_SW
LIBTCG_MO_TESL     = LIBTCG_MO_TE | LIBTCG_MO_SL
LIBTCG_MO_TEQ      = LIBTCG_MO_TE | LIBTCG_MO_Q
LIBTCG_MO_SSIZE    = LIBTCG_MO_SIZE | LIBTCG_MO_SIGN
# } LibTCGMemOp;

ldst_name = {
    LIBTCG_MO_UB: "ub",
    LIBTCG_MO_SB: "sb",
    LIBTCG_MO_LEUW: "leuw",
    LIBTCG_MO_LESW: "lesw",
    LIBTCG_MO_LEUL: "leul",
    LIBTCG_MO_LESL: "lesl",
    LIBTCG_MO_LEQ: "leq",
    LIBTCG_MO_BEUW: "beuw",
    LIBTCG_MO_BESW: "besw",
    LIBTCG_MO_BEUL: "beul",
    LIBTCG_MO_BESL: "besl",
    LIBTCG_MO_BEQ: "beq",
}

alignment_name = {
    (LIBTCG_MO_ALIGN_2 >> LIBTCG_MO_ASHIFT): "al2+",
    (LIBTCG_MO_ALIGN_4 >> LIBTCG_MO_ASHIFT): "al4+",
    (LIBTCG_MO_ALIGN_8 >> LIBTCG_MO_ASHIFT): "al8+",
    (LIBTCG_MO_ALIGN_16 >> LIBTCG_MO_ASHIFT): "al16+",
    (LIBTCG_MO_ALIGN_32 >> LIBTCG_MO_ASHIFT): "al32+",
    (LIBTCG_MO_ALIGN_64 >> LIBTCG_MO_ASHIFT): "al64+",
}

ALIGNED_ONLY = 0

if ALIGNED_ONLY:
    alignment_name[LIBTCG_MO_UNALN >> LIBTCG_MO_ASHIFT] = "un+"
    alignment_name[LIBTCG_MO_ALIGN >> LIBTCG_MO_ASHIFT] = ""
else:
    alignment_name[LIBTCG_MO_UNALN >> LIBTCG_MO_ASHIFT] = ""
    alignment_name[LIBTCG_MO_ALIGN >> LIBTCG_MO_ASHIFT] = "al+"

TARGET_LONG_BITS = 64
TARGET_LONG_SIZE = (TARGET_LONG_BITS/8)

# /* target_ulong is the type of a virtual address */
# #define TARGET_LONG_SIZE (TARGET_LONG_BITS/8)
# #if TARGET_LONG_SIZE == 4
# typedef int32_t target_long;
# typedef uint32_t target_ulong;
# #define TARGET_FMT_lx "%08x"
# #define TARGET_FMT_ld "%d"
# #define TARGET_FMT_lu "%u"
# #elif TARGET_LONG_SIZE == 8
# typedef int64_t target_long;
# typedef uint64_t target_ulong;
# #define TARGET_FMT_lx "%016" PRIx64
# #define TARGET_FMT_ld "%" PRId64
# #define TARGET_FMT_lu "%" PRIu64
# #else
# #error TARGET_LONG_SIZE undefined
# #endif

TARGET_FMT_lx = "%016x"
TARGET_FMT_ld = "%d"
TARGET_FMT_lu = "%u"

def get_memop(oi):
    return oi >> 4

def get_mmuidx(oi):
    return oi & 15

def tcg_dump_ops(s, op, op_def, args):
    c = op.opc
    rep = ''

    if c == lib.LIBTCG_INDEX_op_insn_start:
        rep += '\n\n---'

#         for (i = 0; i < TARGET_INSN_START_WORDS; ++i)
#         {
        for i in range(1): #range(lib.TARGET_INSN_START_WORDS): ???
#             target_ulong a;
# #if TARGET_LONG_BITS > TCG_TARGET_REG_BITS
#             a = ((target_ulong)args[i * 2 + 1] << 32) | args[i * 2];
# #else
#             a = args[i];
            a = args[i]
# #endif
            rep += (' ' + TARGET_FMT_lx) % a
    elif c == lib.LIBTCG_INDEX_op_call:
        # variable number of arguments
        nb_oargs = op.callo
        nb_iargs = op.calli
        nb_cargs = op_def.nb_cargs

        # function name, flags, out args
        rep += ' %s %s,$0x%x,$%d' % (
            ffi.string(op_def.name).decode('utf-8'),
            tcg_find_helper(s, args[nb_oargs + nb_iargs]),
            args[nb_oargs + nb_iargs + 1], nb_oargs)

        for i in range(nb_oargs):
            rep += ',%s' % tcg_get_arg_str_idx(s, args[i])

        for i in range(nb_iargs):
            arg = args[nb_oargs+i]
            t = '<dummy>'
            if arg != -1:
                t = tcg_get_arg_str_idx(s, arg)
            rep += ',%s' % t

    else:
        rep += ' %s ' % ffi.string(op_def.name).decode('utf-8')
        nb_oargs = op_def.nb_oargs
        nb_iargs = op_def.nb_iargs
        nb_cargs = op_def.nb_cargs
        k = 0
        for i in range(nb_oargs):
            if k:
                rep += ','
            rep += tcg_get_arg_str_idx(s, args[k])
            k += 1
        for i in range(nb_iargs):
            if k:
                rep += ','
            rep += tcg_get_arg_str_idx(s, args[k])
            k += 1
        if c in [
            lib.LIBTCG_INDEX_op_brcond_i32,
            lib.LIBTCG_INDEX_op_setcond_i32,
            lib.LIBTCG_INDEX_op_movcond_i32,
            lib.LIBTCG_INDEX_op_brcond2_i32,
            lib.LIBTCG_INDEX_op_setcond2_i32,
            lib.LIBTCG_INDEX_op_brcond_i64,
            lib.LIBTCG_INDEX_op_setcond_i64,
            lib.LIBTCG_INDEX_op_movcond_i64]:
            if args[k] in cond_name:
                rep += ',%s' % cond_name[args[k]]
            else:
                rep += ',$0x%x' % args[k]
            k += 1
            i = 1
        elif c in [
            lib.LIBTCG_INDEX_op_qemu_ld_i32,
            lib.LIBTCG_INDEX_op_qemu_st_i32,
            lib.LIBTCG_INDEX_op_qemu_ld_i64,
            lib.LIBTCG_INDEX_op_qemu_st_i64]:
            oi = args[k]
            k += 1
            mem_op = get_memop(oi)
            ix = get_mmuidx(oi)
            if mem_op & ~(LIBTCG_MO_AMASK | LIBTCG_MO_BSWAP | LIBTCG_MO_SSIZE):
                rep += ",$0x%x,%u" % (op, ix)
            else:
                s_al = alignment_name[(mem_op & LIBTCG_MO_AMASK) >> LIBTCG_MO_ASHIFT];
                s_op = ldst_name[mem_op & (LIBTCG_MO_BSWAP | LIBTCG_MO_SSIZE)];
                rep += ",%s%s,%u" % (s_al, s_op, ix)

            i = 1
        else:
            i = 0
        if c in [
            lib.LIBTCG_INDEX_op_set_label,
            lib.LIBTCG_INDEX_op_br,
            lib.LIBTCG_INDEX_op_brcond_i32,
            lib.LIBTCG_INDEX_op_brcond_i64,
            lib.LIBTCG_INDEX_op_brcond2_i32]:
            rep += "%s$L%d" % ("," if k else "",  arg_label(args[k]).id)
            i += 1
            k += 1

        while i < nb_cargs:
            rep += "%s$0x%x" % ("," if k else "", args[k])
            i += 1
            k += 1
# #if 0 // FIXME
#     if (op->life)
#     {
#         unsigned life = op->life;

#         for (; col < 48; ++col)
#         {
#             putc(' ', qemu_logfile);
#         }

#         if (life & (SYNC_ARG * 3))
#         {
#             qemu_log("  sync:");
#             for (i = 0; i < 2; ++i)
#             {
#                 if (life & (SYNC_ARG << i))
#                 {
#                     qemu_log(" %d", i);
#                 }
#             }
#         }
#         life /= DEAD_ARG;
#         if (life)
#         {
#             qemu_log("  dead:");
#             for (i = 0; life; ++i, life >>= 1)
#             {
#                 if (life & 1)
#                 {
#                     qemu_log(" %d", i);
#                 }
#             }
#         }
#     }
# #endif
#     qemu_log("\n");
# }

    if rep:
        print(rep)

if __name__ == '__main__':
    main()
