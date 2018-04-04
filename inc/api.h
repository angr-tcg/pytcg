typedef long off_t;





typedef signed char int8_t;
typedef short int int16_t;
typedef int int32_t;

typedef long int int64_t;







typedef unsigned char uint8_t;
typedef unsigned short int uint16_t;

typedef unsigned int uint32_t;



typedef unsigned long int uint64_t;
typedef signed char int_least8_t;
typedef short int int_least16_t;
typedef int int_least32_t;

typedef long int int_least64_t;






typedef unsigned char uint_least8_t;
typedef unsigned short int uint_least16_t;
typedef unsigned int uint_least32_t;

typedef unsigned long int uint_least64_t;
typedef signed char int_fast8_t;

typedef long int int_fast16_t;
typedef long int int_fast32_t;
typedef long int int_fast64_t;
typedef unsigned char uint_fast8_t;

typedef unsigned long int uint_fast16_t;
typedef unsigned long int uint_fast32_t;
typedef unsigned long int uint_fast64_t;
typedef long int intptr_t;


typedef unsigned long int uintptr_t;
typedef long int intmax_t;
typedef unsigned long int uintmax_t;







typedef uint8_t LibTCGReg;

typedef uint64_t LibTCGRegSet;
typedef uint64_t tcg_temp;
typedef uint64_t LibTCGArg;

typedef struct LibTCGArgConstraint {
    uint16_t ct;
    uint8_t alias_index;
    union {
        LibTCGRegSet regs;
    } u;
} LibTCGArgConstraint;

typedef enum LibTCGOpcode {

LIBTCG_INDEX_op_discard,
LIBTCG_INDEX_op_set_label,


LIBTCG_INDEX_op_call,

LIBTCG_INDEX_op_br,
LIBTCG_INDEX_op_mb,

LIBTCG_INDEX_op_mov_i32,
LIBTCG_INDEX_op_movi_i32,
LIBTCG_INDEX_op_setcond_i32,
LIBTCG_INDEX_op_movcond_i32,

LIBTCG_INDEX_op_ld8u_i32,
LIBTCG_INDEX_op_ld8s_i32,
LIBTCG_INDEX_op_ld16u_i32,
LIBTCG_INDEX_op_ld16s_i32,
LIBTCG_INDEX_op_ld_i32,
LIBTCG_INDEX_op_st8_i32,
LIBTCG_INDEX_op_st16_i32,
LIBTCG_INDEX_op_st_i32,

LIBTCG_INDEX_op_add_i32,
LIBTCG_INDEX_op_sub_i32,
LIBTCG_INDEX_op_mul_i32,
LIBTCG_INDEX_op_div_i32,
LIBTCG_INDEX_op_divu_i32,
LIBTCG_INDEX_op_rem_i32,
LIBTCG_INDEX_op_remu_i32,
LIBTCG_INDEX_op_div2_i32,
LIBTCG_INDEX_op_divu2_i32,
LIBTCG_INDEX_op_and_i32,
LIBTCG_INDEX_op_or_i32,
LIBTCG_INDEX_op_xor_i32,

LIBTCG_INDEX_op_shl_i32,
LIBTCG_INDEX_op_shr_i32,
LIBTCG_INDEX_op_sar_i32,
LIBTCG_INDEX_op_rotl_i32,
LIBTCG_INDEX_op_rotr_i32,
LIBTCG_INDEX_op_deposit_i32,
LIBTCG_INDEX_op_extract_i32,
LIBTCG_INDEX_op_sextract_i32,

LIBTCG_INDEX_op_brcond_i32,

LIBTCG_INDEX_op_add2_i32,
LIBTCG_INDEX_op_sub2_i32,
LIBTCG_INDEX_op_mulu2_i32,
LIBTCG_INDEX_op_muls2_i32,
LIBTCG_INDEX_op_muluh_i32,
LIBTCG_INDEX_op_mulsh_i32,
LIBTCG_INDEX_op_brcond2_i32,
LIBTCG_INDEX_op_setcond2_i32,

LIBTCG_INDEX_op_ext8s_i32,
LIBTCG_INDEX_op_ext16s_i32,
LIBTCG_INDEX_op_ext8u_i32,
LIBTCG_INDEX_op_ext16u_i32,
LIBTCG_INDEX_op_bswap16_i32,
LIBTCG_INDEX_op_bswap32_i32,
LIBTCG_INDEX_op_not_i32,
LIBTCG_INDEX_op_neg_i32,
LIBTCG_INDEX_op_andc_i32,
LIBTCG_INDEX_op_orc_i32,
LIBTCG_INDEX_op_eqv_i32,
LIBTCG_INDEX_op_nand_i32,
LIBTCG_INDEX_op_nor_i32,
LIBTCG_INDEX_op_clz_i32,
LIBTCG_INDEX_op_ctz_i32,
LIBTCG_INDEX_op_ctpop_i32,

LIBTCG_INDEX_op_mov_i64,
LIBTCG_INDEX_op_movi_i64,
LIBTCG_INDEX_op_setcond_i64,
LIBTCG_INDEX_op_movcond_i64,

LIBTCG_INDEX_op_ld8u_i64,
LIBTCG_INDEX_op_ld8s_i64,
LIBTCG_INDEX_op_ld16u_i64,
LIBTCG_INDEX_op_ld16s_i64,
LIBTCG_INDEX_op_ld32u_i64,
LIBTCG_INDEX_op_ld32s_i64,
LIBTCG_INDEX_op_ld_i64,
LIBTCG_INDEX_op_st8_i64,
LIBTCG_INDEX_op_st16_i64,
LIBTCG_INDEX_op_st32_i64,
LIBTCG_INDEX_op_st_i64,

LIBTCG_INDEX_op_add_i64,
LIBTCG_INDEX_op_sub_i64,
LIBTCG_INDEX_op_mul_i64,
LIBTCG_INDEX_op_div_i64,
LIBTCG_INDEX_op_divu_i64,
LIBTCG_INDEX_op_rem_i64,
LIBTCG_INDEX_op_remu_i64,
LIBTCG_INDEX_op_div2_i64,
LIBTCG_INDEX_op_divu2_i64,
LIBTCG_INDEX_op_and_i64,
LIBTCG_INDEX_op_or_i64,
LIBTCG_INDEX_op_xor_i64,

LIBTCG_INDEX_op_shl_i64,
LIBTCG_INDEX_op_shr_i64,
LIBTCG_INDEX_op_sar_i64,
LIBTCG_INDEX_op_rotl_i64,
LIBTCG_INDEX_op_rotr_i64,
LIBTCG_INDEX_op_deposit_i64,
LIBTCG_INDEX_op_extract_i64,
LIBTCG_INDEX_op_sextract_i64,


LIBTCG_INDEX_op_ext_i32_i64,
LIBTCG_INDEX_op_extu_i32_i64,
LIBTCG_INDEX_op_extrl_i64_i32,


LIBTCG_INDEX_op_extrh_i64_i32,



LIBTCG_INDEX_op_brcond_i64,
LIBTCG_INDEX_op_ext8s_i64,
LIBTCG_INDEX_op_ext16s_i64,
LIBTCG_INDEX_op_ext32s_i64,
LIBTCG_INDEX_op_ext8u_i64,
LIBTCG_INDEX_op_ext16u_i64,
LIBTCG_INDEX_op_ext32u_i64,
LIBTCG_INDEX_op_bswap16_i64,
LIBTCG_INDEX_op_bswap32_i64,
LIBTCG_INDEX_op_bswap64_i64,
LIBTCG_INDEX_op_not_i64,
LIBTCG_INDEX_op_neg_i64,
LIBTCG_INDEX_op_andc_i64,
LIBTCG_INDEX_op_orc_i64,
LIBTCG_INDEX_op_eqv_i64,
LIBTCG_INDEX_op_nand_i64,
LIBTCG_INDEX_op_nor_i64,
LIBTCG_INDEX_op_clz_i64,
LIBTCG_INDEX_op_ctz_i64,
LIBTCG_INDEX_op_ctpop_i64,

LIBTCG_INDEX_op_add2_i64,
LIBTCG_INDEX_op_sub2_i64,
LIBTCG_INDEX_op_mulu2_i64,
LIBTCG_INDEX_op_muls2_i64,
LIBTCG_INDEX_op_muluh_i64,
LIBTCG_INDEX_op_mulsh_i64,





LIBTCG_INDEX_op_insn_start,

LIBTCG_INDEX_op_exit_tb,
LIBTCG_INDEX_op_goto_tb,

LIBTCG_INDEX_op_qemu_ld_i32,

LIBTCG_INDEX_op_qemu_st_i32,

LIBTCG_INDEX_op_qemu_ld_i64,

LIBTCG_INDEX_op_qemu_st_i64,

    LIBTCG_NB_OPS,
} LibTCGOpcode;

typedef enum LibTCGTempVal {
    LIBTCG_TEMP_VAL_DEAD,
    LIBTCG_TEMP_VAL_REG,
    LIBTCG_TEMP_VAL_MEM,
    LIBTCG_TEMP_VAL_CONST,
} LibTCGTempVal;

typedef enum LibTCGType {
    LIBTCG_TYPE_I32,
    LIBTCG_TYPE_I64,
    LIBTCG_TYPE_COUNT,






    LIBTCG_TYPE_REG = LIBTCG_TYPE_I64,






    LIBTCG_TYPE_PTR = LIBTCG_TYPE_I64,
} LibTCGType;

typedef struct LibTCGTemp {
    LibTCGReg reg:8;
    LibTCGTempVal val_type:8;
    LibTCGType base_type:8;
    LibTCGType type:8;
    unsigned int fixed_reg:1;
    unsigned int indirect_reg:1;
    unsigned int indirect_base:1;
    unsigned int mem_coherent:1;
    unsigned int mem_allocated:1;
    unsigned int temp_local:1;


    unsigned int temp_allocated:1;

    tcg_temp val;
    struct LibTCGTemp *mem_base;
    intptr_t mem_offset;
    const char *name;
} LibTCGTemp;

typedef struct LibTCGOpDef {
    const char *name;
    uint8_t nb_oargs, nb_iargs, nb_cargs, nb_args;
    uint8_t flags;
    LibTCGArgConstraint *args_ct;
    int *sorted_args;



} LibTCGOpDef;






/*
typedef enum {

    LIBTCG_COND_NEVER = 0 | 0 | 0 | 0,
    LIBTCG_COND_ALWAYS = 0 | 0 | 0 | 1,
    LIBTCG_COND_EQ = 8 | 0 | 0 | 0,
    LIBTCG_COND_NE = 8 | 0 | 0 | 1,

    LIBTCG_COND_LT = 0 | 0 | 2 | 0,
    LIBTCG_COND_GE = 0 | 0 | 2 | 1,
    LIBTCG_COND_LE = 8 | 0 | 2 | 0,
    LIBTCG_COND_GT = 8 | 0 | 2 | 1,

    LIBTCG_COND_LTU = 0 | 4 | 0 | 0,
    LIBTCG_COND_GEU = 0 | 4 | 0 | 1,
    LIBTCG_COND_LEU = 8 | 4 | 0 | 0,
    LIBTCG_COND_GTU = 8 | 4 | 0 | 1,
} LibTCGCond;


typedef enum LibTCGMemOp {
    LIBTCG_MO_8 = 0,
    LIBTCG_MO_16 = 1,
    LIBTCG_MO_32 = 2,
    LIBTCG_MO_64 = 3,
    LIBTCG_MO_SIZE = 3,

    LIBTCG_MO_SIGN = 4,

    LIBTCG_MO_BSWAP = 8,





    LIBTCG_MO_LE = 0,
    LIBTCG_MO_BE = LIBTCG_MO_BSWAP,




    LIBTCG_MO_TE = LIBTCG_MO_LE,
    LIBTCG_MO_ASHIFT = 4,
    LIBTCG_MO_AMASK = 7 << LIBTCG_MO_ASHIFT,




    LIBTCG_MO_ALIGN = LIBTCG_MO_AMASK,
    LIBTCG_MO_UNALN = 0,

    LIBTCG_MO_ALIGN_2 = 1 << LIBTCG_MO_ASHIFT,
    LIBTCG_MO_ALIGN_4 = 2 << LIBTCG_MO_ASHIFT,
    LIBTCG_MO_ALIGN_8 = 3 << LIBTCG_MO_ASHIFT,
    LIBTCG_MO_ALIGN_16 = 4 << LIBTCG_MO_ASHIFT,
    LIBTCG_MO_ALIGN_32 = 5 << LIBTCG_MO_ASHIFT,
    LIBTCG_MO_ALIGN_64 = 6 << LIBTCG_MO_ASHIFT,


    LIBTCG_MO_UB = LIBTCG_MO_8,
    LIBTCG_MO_UW = LIBTCG_MO_16,
    LIBTCG_MO_UL = LIBTCG_MO_32,
    LIBTCG_MO_SB = LIBTCG_MO_SIGN | LIBTCG_MO_8,
    LIBTCG_MO_SW = LIBTCG_MO_SIGN | LIBTCG_MO_16,
    LIBTCG_MO_SL = LIBTCG_MO_SIGN | LIBTCG_MO_32,
    LIBTCG_MO_Q = LIBTCG_MO_64,

    LIBTCG_MO_LEUW = LIBTCG_MO_LE | LIBTCG_MO_UW,
    LIBTCG_MO_LEUL = LIBTCG_MO_LE | LIBTCG_MO_UL,
    LIBTCG_MO_LESW = LIBTCG_MO_LE | LIBTCG_MO_SW,
    LIBTCG_MO_LESL = LIBTCG_MO_LE | LIBTCG_MO_SL,
    LIBTCG_MO_LEQ = LIBTCG_MO_LE | LIBTCG_MO_Q,

    LIBTCG_MO_BEUW = LIBTCG_MO_BE | LIBTCG_MO_UW,
    LIBTCG_MO_BEUL = LIBTCG_MO_BE | LIBTCG_MO_UL,
    LIBTCG_MO_BESW = LIBTCG_MO_BE | LIBTCG_MO_SW,
    LIBTCG_MO_BESL = LIBTCG_MO_BE | LIBTCG_MO_SL,
    LIBTCG_MO_BEQ = LIBTCG_MO_BE | LIBTCG_MO_Q,

    LIBTCG_MO_TEUW = LIBTCG_MO_TE | LIBTCG_MO_UW,
    LIBTCG_MO_TEUL = LIBTCG_MO_TE | LIBTCG_MO_UL,
    LIBTCG_MO_TESW = LIBTCG_MO_TE | LIBTCG_MO_SW,
    LIBTCG_MO_TESL = LIBTCG_MO_TE | LIBTCG_MO_SL,
    LIBTCG_MO_TEQ = LIBTCG_MO_TE | LIBTCG_MO_Q,

    LIBTCG_MO_SSIZE = LIBTCG_MO_SIZE | LIBTCG_MO_SIGN,

} LibTCGMemOp;
*/

typedef int LibTCGCond;
typedef int LibTCGMemOp;

typedef struct LibTCGHelperInfo
{
    void *func;
    const char *name;
    unsigned flags;
    unsigned sizemask;
} LibTCGHelperInfo;
typedef struct LibTCGOp {
    LibTCGOpcode opc:8;


    unsigned calli:4;
    unsigned callo:2;

    LibTCGArg *args;
} LibTCGOp;





typedef struct {
    LibTCGOp *instructions;
    unsigned instruction_count;


    LibTCGArg *arguments;
    LibTCGTemp *temps;
    unsigned global_temps;
    unsigned total_temps;
} LibTCGInstructions;





typedef struct {
    uint64_t virtual_address;
    void *pointer;
} address_pair;
typedef address_pair (*libtcg_mmap_func)(uint64_t start, uint64_t len, int prot,
                                         int flags, int fd, off_t offset);
typedef LibTCGInstructions (*libtcg_translate_func)(uint64_t virtual_address);




typedef void (*libtcg_free_instructions_func)(LibTCGInstructions *instructions);

typedef LibTCGHelperInfo *(*libtcg_find_helper_func)(uintptr_t val);

typedef struct {
    libtcg_mmap_func mmap;
    libtcg_translate_func translate;
    libtcg_free_instructions_func free_instructions;
    libtcg_find_helper_func find_helper;
} LibTCGInterface;
typedef const LibTCGInterface *(*libtcg_init_func)(const char *cpu_name,
                                                   intptr_t start_address);

struct tcg_insn_unit;
typedef struct tcg_insn_unit tcg_insn_unit;

typedef struct TCGRelocation {
    struct TCGRelocation *next;
    int type;
    tcg_insn_unit *ptr;
    intptr_t addend;
} TCGRelocation; 

typedef struct TCGLabel {
    unsigned has_value : 1;
    unsigned id : 31;
    union {
        uintptr_t value;
        tcg_insn_unit *value_ptr;
        TCGRelocation *first_reloc;
    } u;
} TCGLabel;
