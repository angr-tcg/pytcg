# FFI interface to libtcg (run build_ffi first)
from __future__ import print_function
from libtcg import ffi, lib
import ctypes
import sys
import argparse
import archinfo
import os.path

libc_so = {"darwin": "libc.dylib", "linux": "", "linux2": ""}[sys.platform]
libc = ctypes.CDLL(libc_so, use_errno=True, use_last_error=True)

# void *dlopen(const char *filename, int flags);
dlopen = libc.dlopen
dlopen.restype = ctypes.c_void_p
dlopen.argtypes = (ctypes.c_char_p, ctypes.c_int)

# void *dlsym(void *handle, const char *symbol);
dlsym = libc.dlsym
dlsym.restype = ctypes.c_void_p
dlsym.argtypes = (ctypes.c_void_p, ctypes.c_char_p)

# Load the lib
path_to_libtcg = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'libtcg', 'libtcg-x86_64.so.2.8.50')
libtcg_so = dlopen(path_to_libtcg.encode('utf-8'), 1)
assert(libtcg_so is not None)

# Resolve libtcg_init
libtcg_init = dlsym(libtcg_so, "libtcg_init".encode('utf-8'))
assert(libtcg_init is not None)

libtcg_init_func = ffi.cast('libtcg_init_func', libtcg_init)

tcg = libtcg_init_func(b'qemu64', 0xb0000000)
assert(tcg is not None)

class Tb(object):
    # LibTCGOp *instructions;
    # unsigned instruction_count;
    # LibTCGArg *arguments;
    # LibTCGTemp *temps;
    # unsigned global_temps;
    # unsigned total_temps;
    def __init__(self):
        pass

class TcgTemp(object):
    # LibTCGReg reg:8;
    # LibTCGTempVal val_type:8;
    # LibTCGType base_type:8;
    # LibTCGType type:8;
    # unsigned int fixed_reg:1;
    # unsigned int indirect_reg:1;
    # unsigned int indirect_base:1;
    # unsigned int mem_coherent:1;
    # unsigned int mem_allocated:1;
    # unsigned int temp_local:1;
    # unsigned int temp_allocated:1;
    # tcg_temp val;
    # struct LibTCGTemp *mem_base;
    # intptr_t mem_offset;
    # const char *name;
    pass

class TcgOp(object):
    def __init__(self, op_def, opc, calli, callo, args):
        self.op_def = op_def
        self.opc = opc
        self.calli = calli
        self.callo = callo
        self.args = args

    @classmethod
    def from_LibTCGOp(cls, lto):
        op_def = lib.tcg_op_defs[lto.opc]
        # name = ffi.string(op_def.name)
        # FIXME: Args array should be op_def
        return TcgOp(op_def, lto.opc, lto.calli, lto.callo, [])

class IRSB(object):
    def __init__(self, data, mem_addr, arch, max_inst=None, max_bytes=None, bytes_offset=0, traceflags=0, opt_level=1, num_inst=None, num_bytes=None):
        # FIXME: Unsupported interfaces
        assert(arch == archinfo.ArchAMD64()) # FIXME: Should support multiple architectures
        assert(max_inst is None)
        assert(max_bytes is None)
        assert(traceflags == 0)
        assert(opt_level == 1)
        assert(num_inst is None)
        # FIXME: angr will pass len(data), but libtcg has no way to limit the
        # number of instructions decoded (it'll go until it hits a branch),
        # go fix it!)
        # assert(num_bytes is None) 
        self.arch = arch
        self.addr = mem_addr
        self.size = len(data)

        self._instructions = None

        #
        # Perform the lifting
        #

        # Map in a page we can write to
        self.address = tcg.mmap(mem_addr, 4096, 3, 0x22, -1, 0)
        assert(self.address.virtual_address == mem_addr)

        # Copy in data
        dest = int(ffi.cast("uintptr_t", self.address.pointer))
        ctypes.memmove(dest, data, len(data))

        # Translate block of instructions starting at bytes_offset
        self._tb = tcg.translate(self.address.virtual_address + bytes_offset)

        self._global_temps = self._tb.global_temps
        self._total_temps = self._tb.total_temps
        self._virt_addr = self.address.virtual_address
        self._num_ops = self._tb.instruction_count
        
        ops = []
        for i in range(self._tb.instruction_count):
            op = self._tb.instructions[i]
            ops.append(TcgOp.from_LibTCGOp(op))

        if False:
            print("global_temps: %d" % self._global_temps)
            print("total_temps:  %d" % self._total_temps)
            print("virtual_addr: 0x%x" % self._virt_addr)
            print("num ops:      %d" % self._num_ops)
            print('')

            for i in range(self._total_temps):
                print('temp #%d = %s' % (i, tcg_get_arg_str_idx(self._tb, i)))

                print('  reg.............: %d' % self._tb.temps[i].reg)
                print('  val_type........: %d' % self._tb.temps[i].val_type)
                print('  base_type.......: %d' % self._tb.temps[i].base_type)
                print('  type............: %d' % self._tb.temps[i].type)
                print('  fixed_reg.......: %d' % self._tb.temps[i].fixed_reg)
                print('  indirect_reg....: %d' % self._tb.temps[i].indirect_reg)
                print('  indirect_base...: %d' % self._tb.temps[i].indirect_base)
                print('  mem_coherent....: %d' % self._tb.temps[i].mem_coherent)
                print('  mem_allocated...: %d' % self._tb.temps[i].mem_allocated)
                print('  temp_local......: %d' % self._tb.temps[i].temp_local)
                print('  temp_allocated..: %d' % self._tb.temps[i].temp_allocated)
                print('  val.............: %d' % self._tb.temps[i].val)
                #print('  mem_base........: %d' % self._tb.temps[i].mem_base)
                print('  mem_offset......: %d' % self._tb.temps[i].mem_offset)
                #print('  name............: %d' % self._tb.temps[i].name)
        
            print('')

    def __del__(self):
        tcg.free_instructions(ffi.addressof(self._tb))
    
    def _pp_str(self):
        s = []
        for i in range(self._tb.instruction_count):
            op = self._tb.instructions[i]
            op_def = lib.tcg_op_defs[op.opc]
            # name = ffi.string(op_def.name)
            s.append(tcg_dump_ops(self._tb, op, op_def, op.args))
        return '\n'.join(s)

    def pp(self):
        """
        Pretty-print the IRSB to stdout.
        """
        print(self._pp_str())

    def __repr__(self):
        return 'IRSB <0x%x bytes, %d ins., %s> at 0x%x' % (self.size, self.instructions, str(self.arch), self.addr)

    def __str__(self):
        return self._pp_str()

    @property
    def instructions(self):
        """
        The number of instructions in this block
        """
        if self._instructions is None:
            # FIXME: This ugliness should be trivially calculated when we first
            # create the IRSB (really, the instruction decode in qemu should
            # tell us, but _you_ need to go surface that out through the tb
            # struct)
            # self._instructions = len([s for s in self.statements if type(s) is stmt.IMark])
            self._instructions = 0
            for i in range(self._tb.instruction_count): # TCG Op count (not guest)
                op = self._tb.instructions[i]
                if op.opc == lib.LIBTCG_INDEX_op_insn_start:
                    self._instructions += 1

        return self._instructions

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('arch')
    ap.add_argument('mem_addr', type=lambda x:int(x, 0))
    args = ap.parse_args()

    data = open(args.file, 'rb').read()
    assert(args.arch == 'amd64')
    irsb = IRSB(data, args.mem_addr, archinfo.ArchAMD64())
    irsb.pp()

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
        rep += '@'

        TARGET_INSN_START_WORDS = 2
        for i in range(TARGET_INSN_START_WORDS):
            # if lib.TARGET_LONG_BITS > lib.TCG_TARGET_REG_BITS:
            #     # a = ((target_ulong)args[i * 2 + 1] << 32) | args[i * 2];
            #     assert(False)
            # else:
            a = args[i]
            rep += (' 0x' + TARGET_FMT_lx) % a
    elif c == lib.LIBTCG_INDEX_op_call:
        # variable number of arguments
        nb_oargs = op.callo
        nb_iargs = op.calli
        nb_cargs = op_def.nb_cargs

        # function name, flags, out args
        rep += '%s %s,$0x%x,$%d' % (
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
        rep += '%s ' % ffi.string(op_def.name).decode('utf-8')
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

    return rep

if __name__ == '__main__':
    main()
