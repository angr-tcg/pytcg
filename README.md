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

## Run

There's a simple Makefile to build the FFI and run basic interface testing.

## Example op pretty-print

"#" Prefixes a comment
"---" Denotes an original instruction boundary address

```
# mov ecx, 0x3290
--- 00000000b0000000 0000000000000000
 movi_i64 tmp0,$0x3290
 ext32u_i64 rcx,tmp0

# mov dword [esi], ecx
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
 call glue(glue(atomic_, xchg), q_be),$0x20,$1,cc_src,cc_dst,cc_src,cc_src2,cc_op
 mov_i64 cc_dst,tmp0
 discard cc_src2
 discard cc_op

# jnz loop
--- 00000000b0000008 0000000000000020
 ext32u_i64 tmp0,cc_dst
 movi_i32 cc_op,$0x20
 movi_i64 tmp11,$0x0
 brcond_i64 tmp0,tmp11,ne,$L0
 goto_tb $0x0
 movi_i64 tmp3,$0xb000000a
 st_i64 tmp3,env,$0x80
 exit_tb $0x7ffff15a5010
 set_label $L0
 goto_tb $0x1
 movi_i64 tmp3,$0xb0000005
 st_i64 tmp3,env,$0x80
 exit_tb $0x7ffff15a5011
```
