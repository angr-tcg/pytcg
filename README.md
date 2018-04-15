pytcg
=====

Status: Very early, but working!  So far it's able to translate from 32-bit x86
to TCG ops and print out some op info. Pythonification is next!

## Build libtcg

Before using pytcg, you'll need to build libtcg. You can do this by:

    cd libtcg
    ./build.sh

This will clone the Qemu repository with the libtcg patches, build, and extract
the necessary files into this directory.

See the [libtcg](https://github.com/angr-tcg/qemu) repo for more info.

## Setup Python Virtual Environment

Setup your Python virtual environment with something like:

    sudo apt-get install python3-venv
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt

If you have the angr virtual environment already set up, you can use that too
(via `workon angr`) since the pytcg requirements are a subset of angr's.

## Run

There's a simple Makefile to build the FFI and run basic interface testing:

    make

## Overview of Qemu sources

Libtcg interface is located at qemu/libtcg/libtcg.c. The frontend (which does
guest binary to TCG translation) is located at qemu/target/i386/translate.c.

## Debugging Qemu

If you want to step through the real TCG generation code, fire up ipython in
one terminal, get the process id, then in another terminal fire up gdb and
attach to the ipython process. Then you can set breakpoints on code generation
functions, etc.

## Example op pretty-print

Input assembly:
```
     1                                  bits 32
     2                                  org 0xb0000000
     3                                  
     4 00000000 B990320000              mov ecx, 0x3290
     5                                  loop:
     6 00000005 890E                    mov dword [esi], ecx
     7 00000007 49                      dec ecx
     8 00000008 75FB                    jnz loop
```

* `#` Prefixes a comment
* `---` Denotes an original instruction boundary address

```
# mov ecx, 0x3290
--- 00000000b0000000 0000000000000000
 movi_i64 tmp0,$0x3290
 ext32u_i64 rcx,tmp0

# loop: mov dword [esi], ecx
--- 00000000b0000005 0000000000000000
 add_i64 tmp2,rsi,ds_base
 ext32u_i64 tmp2,tmp2
 mov_i64 tmp0,rcx
 qemu_st_i64 tmp0,tmp2,leul,0


# dec ecx
--- 00000000b0000007 0000000000000000
 mov_i64 tmp0,rcx
 movi_i64 tmp11,$0xffffffffffffffff
 add_i64 tmp0,tmp0,tmp11
 ext32u_i64 rcx,tmp0
 call cc_compute_c,$0x50,$1,cc_src,cc_dst,cc_src,cc_src2,cc_op
 mov_i64 cc_dst,tmp0
 discard cc_src2
 discard cc_op


# jnz loop
--- 00000000b0000008 0000000000000020
 ext32u_i64 tmp0,cc_dst
 movi_i32 cc_op,$0x20
 movi_i64 tmp11,$0x0
 brcond_i64 tmp0,tmp11,ne,$L0
 
 movi_i64 tmp3,$0xb000000a   # Load address of next EIP (jump not taken)
 st_i64 tmp3,env,$0x80       # Load addr into EIP (stored in env+0x80)
 br $L1                      # Jump to end of block
 
 set_label $L0
 movi_i64 tmp3,$0xb0000005   # Load address of next EIP (jump taken)
 st_i64 tmp3,env,$0x80       # Load addr into EIP (stored in env+0x80)
 
 set_label $L1
 exit_tb $0x0
```

For reference, PyVEX's IR of the same code (very similar of course):
```
import angr
main_opts = {
    'backend': 'blob',
    'custom_arch': 'amd64',
    'custom_entry_point': 0xb0000000,
    'custom_base_addr': 0xb0000000,
}
p = angr.Project('pytcg/test/simple_loop.bin', auto_load_libs=False, main_opts=main_opts)
s = p.factory.entry_state()
b = s.block()
b.vex.pp()

IRSB {
   t0:Ity_I64 t1:Ity_I64 t2:Ity_I32 t3:Ity_I64 t4:Ity_I1 t5:Ity_I64 t6:Ity_I64 t7:Ity_I64 t8:Ity_I64 t9:Ity_I64 t10:Ity_I64

   00 | ------ IMark(0xb0000000, 5, 0) ------
   01 | PUT(rcx) = 0x0000000000003290
   02 | PUT(pc) = 0x00000000b0000005
   03 | ------ IMark(0xb0000005, 2, 0) ------
   04 | t0 = GET:I64(rsi)
   05 | STle(t0) = 0x00003290
   06 | PUT(pc) = 0x00000000b0000007
   07 | ------ IMark(0xb0000007, 3, 0) ------
   08 | t5 = GET:I64(cc_op)
   09 | t6 = GET:I64(cc_dep1)
   10 | t7 = GET:I64(cc_dep2)
   11 | t8 = GET:I64(cc_ndep)
   12 | t9 = amd64g_calculate_condition(0x0000000000000004,t5,t6,t7,t8):Ity_I64
   13 | t4 = 64to1(t9)
   14 | if (t4) { PUT(pc) = 0xb000000a; Ijk_Boring }
   NEXT: PUT(rip) = 0x00000000b0000005; Ijk_Boring
}
```
