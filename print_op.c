
#define qemu_log printf

static void pstrcpy(char *buf, int buf_size, const char *str)
{
    int c;
    char *q = buf;

    if (buf_size <= 0)
        return;

    for (;;)
    {
        c = *str++;
        if (c == 0 || q >= buf + buf_size - 1)
            break;
        *q++ = c;
    }
    *q = '\0';
}

static inline int temp_idx(LibTCGInstructions *s, LibTCGTemp *ts)
{
    ptrdiff_t n = ts - s->temps;
    tcg_debug_assert(n >= 0 && n < s->total_temps);
    return n;
}

static char *tcg_get_arg_str_ptr(LibTCGInstructions *s, char *buf, int buf_size,
                                 LibTCGTemp *ts)
{
    int idx = temp_idx(s, ts);

    if (idx < s->global_temps)
    {
        pstrcpy(buf, buf_size, ts->name);
    }
    else if (ts->temp_local)
    {
        snprintf(buf, buf_size, "loc%d", idx - s->global_temps);
    }
    else
    {
        snprintf(buf, buf_size, "tmp%d", idx - s->global_temps);
    }
    return buf;
}

static char *tcg_get_arg_str_idx(LibTCGInstructions *s, char *buf,
                                 int buf_size, int idx)
{
    tcg_debug_assert(idx >= 0 && idx < s->total_temps);
    return tcg_get_arg_str_ptr(s, buf, buf_size, &s->temps[idx]);
}

/* Find helper name.  */
static inline const char *tcg_find_helper(LibTCGInstructions *s, uintptr_t val)
{
    const char *ret = NULL;
    // if (s->helpers)
    // {
    //     TCGHelperInfo *info = g_hash_table_lookup(s->helpers, (gpointer)val);
    //     if (info)
    //     {
    //         ret = info->name;
    //     }
    // }
    return ret;
}

static const char *const cond_name[] =
    {
        [LIBTCG_COND_NEVER] = "never",
        [LIBTCG_COND_ALWAYS] = "always",
        [LIBTCG_COND_EQ] = "eq",
        [LIBTCG_COND_NE] = "ne",
        [LIBTCG_COND_LT] = "lt",
        [LIBTCG_COND_GE] = "ge",
        [LIBTCG_COND_LE] = "le",
        [LIBTCG_COND_GT] = "gt",
        [LIBTCG_COND_LTU] = "ltu",
        [LIBTCG_COND_GEU] = "geu",
        [LIBTCG_COND_LEU] = "leu",
        [LIBTCG_COND_GTU] = "gtu"};

static const char *const ldst_name[] =
    {
        [LIBTCG_MO_UB] = "ub",
        [LIBTCG_MO_SB] = "sb",
        [LIBTCG_MO_LEUW] = "leuw",
        [LIBTCG_MO_LESW] = "lesw",
        [LIBTCG_MO_LEUL] = "leul",
        [LIBTCG_MO_LESL] = "lesl",
        [LIBTCG_MO_LEQ] = "leq",
        [LIBTCG_MO_BEUW] = "beuw",
        [LIBTCG_MO_BESW] = "besw",
        [LIBTCG_MO_BEUL] = "beul",
        [LIBTCG_MO_BESL] = "besl",
        [LIBTCG_MO_BEQ] = "beq",
};

static const char *const alignment_name[(LIBTCG_MO_AMASK >> LIBTCG_MO_ASHIFT) + 1] = {
#ifdef ALIGNED_ONLY
    [LIBTCG_MO_UNALN >> LIBTCG_MO_ASHIFT] = "un+",
    [LIBTCG_MO_ALIGN >> LIBTCG_MO_ASHIFT] = "",
#else
    [LIBTCG_MO_UNALN >> LIBTCG_MO_ASHIFT] = "",
    [LIBTCG_MO_ALIGN >> LIBTCG_MO_ASHIFT] = "al+",
#endif
    [LIBTCG_MO_ALIGN_2 >> LIBTCG_MO_ASHIFT] = "al2+",
    [LIBTCG_MO_ALIGN_4 >> LIBTCG_MO_ASHIFT] = "al4+",
    [LIBTCG_MO_ALIGN_8 >> LIBTCG_MO_ASHIFT] = "al8+",
    [LIBTCG_MO_ALIGN_16 >> LIBTCG_MO_ASHIFT] = "al16+",
    [LIBTCG_MO_ALIGN_32 >> LIBTCG_MO_ASHIFT] = "al32+",
    [LIBTCG_MO_ALIGN_64 >> LIBTCG_MO_ASHIFT] = "al64+",
};

/* target_ulong is the type of a virtual address */
#define TARGET_LONG_SIZE (TARGET_LONG_BITS/8)
#if TARGET_LONG_SIZE == 4
typedef int32_t target_long;
typedef uint32_t target_ulong;
#define TARGET_FMT_lx "%08x"
#define TARGET_FMT_ld "%d"
#define TARGET_FMT_lu "%u"
#elif TARGET_LONG_SIZE == 8
typedef int64_t target_long;
typedef uint64_t target_ulong;
#define TARGET_FMT_lx "%016" PRIx64
#define TARGET_FMT_ld "%" PRId64
#define TARGET_FMT_lu "%" PRIu64
#else
#error TARGET_LONG_SIZE undefined
#endif

#define ARRAY_SIZE(x) (sizeof(x)/sizeof(x[0]))

void tcg_dump_ops(LibTCGInstructions *s, LibTCGOp *op, LibTCGOpDef *def, LibTCGArg *args)
{
    char buf[128];

    int i, k, nb_oargs, nb_iargs, nb_cargs;
    LibTCGOpcode c;
    int col = 0;

    c = op->opc;

    if (c == LIBTCG_INDEX_op_insn_start)
    {
        // col += qemu_log("%s ----", oi != s->gen_op_buf[0].next ? "\n" : "");
        col += printf("\n---");

        for (i = 0; i < TARGET_INSN_START_WORDS; ++i)
        {
            target_ulong a;
#if TARGET_LONG_BITS > TCG_TARGET_REG_BITS
            a = ((target_ulong)args[i * 2 + 1] << 32) | args[i * 2];
#else
            a = args[i];
#endif
            col += qemu_log(" " TARGET_FMT_lx, a);
        }
    }
    else if (c == LIBTCG_INDEX_op_call)
    {
        /* variable number of arguments */
        nb_oargs = op->callo;
        nb_iargs = op->calli;
        nb_cargs = def->nb_cargs;

        /* function name, flags, out args */
        col += qemu_log(" %s %s,$0x%" TCG_PRIlx ",$%d", def->name,
                        tcg_find_helper(s, args[nb_oargs + nb_iargs]),
                        args[nb_oargs + nb_iargs + 1], nb_oargs);
        for (i = 0; i < nb_oargs; i++)
        {
            col += qemu_log(",%s", tcg_get_arg_str_idx(s, buf, sizeof(buf),
                                                        args[i]));
        }
        for (i = 0; i < nb_iargs; i++)
        {
            LibTCGArg arg = args[nb_oargs + i];
            const char *t = "<dummy>";
            if (arg != TCG_CALL_DUMMY_ARG)
            {
                t = tcg_get_arg_str_idx(s, buf, sizeof(buf), arg);
            }
            col += qemu_log(",%s", t);
        }
    }
    else
    {
        col += qemu_log(" %s ", def->name);

        nb_oargs = def->nb_oargs;
        nb_iargs = def->nb_iargs;
        nb_cargs = def->nb_cargs;

        k = 0;
        for (i = 0; i < nb_oargs; i++)
        {
            if (k != 0)
            {
                col += qemu_log(",");
            }
            col += qemu_log("%s", tcg_get_arg_str_idx(s, buf, sizeof(buf),
                                                        args[k++]));
        }
        for (i = 0; i < nb_iargs; i++)
        {
            if (k != 0)
            {
                col += qemu_log(",");
            }
            col += qemu_log("%s", tcg_get_arg_str_idx(s, buf, sizeof(buf),
                                                        args[k++]));
        }
        switch (c)
        {
        case LIBTCG_INDEX_op_brcond_i32:
        case LIBTCG_INDEX_op_setcond_i32:
        case LIBTCG_INDEX_op_movcond_i32:
        case LIBTCG_INDEX_op_brcond2_i32:
        case LIBTCG_INDEX_op_setcond2_i32:
        case LIBTCG_INDEX_op_brcond_i64:
        case LIBTCG_INDEX_op_setcond_i64:
        case LIBTCG_INDEX_op_movcond_i64:
            if (args[k] < ARRAY_SIZE(cond_name) && cond_name[args[k]])
            {
                col += qemu_log(",%s", cond_name[args[k++]]);
            }
            else
            {
                col += qemu_log(",$0x%" TCG_PRIlx, args[k++]);
            }
            i = 1;
            break;
        case LIBTCG_INDEX_op_qemu_ld_i32:
        case LIBTCG_INDEX_op_qemu_st_i32:
        case LIBTCG_INDEX_op_qemu_ld_i64:
        case LIBTCG_INDEX_op_qemu_st_i64:
        {
            TCGMemOpIdx oi = args[k++];
            LibTCGMemOp op = get_memop(oi);
            unsigned ix = get_mmuidx(oi);

            if (op & ~(LIBTCG_MO_AMASK | LIBTCG_MO_BSWAP | LIBTCG_MO_SSIZE))
            {
                col += qemu_log(",$0x%x,%u", op, ix);
            }
            else
            {
                const char *s_al, *s_op;
                s_al = alignment_name[(op & LIBTCG_MO_AMASK) >> LIBTCG_MO_ASHIFT];
                s_op = ldst_name[op & (LIBTCG_MO_BSWAP | LIBTCG_MO_SSIZE)];
                col += qemu_log(",%s%s,%u", s_al, s_op, ix);
            }
            i = 1;
        }
        break;
        default:
            i = 0;
            break;
        }
        switch (c)
        {
        case LIBTCG_INDEX_op_set_label:
        case LIBTCG_INDEX_op_br:
        case LIBTCG_INDEX_op_brcond_i32:
        case LIBTCG_INDEX_op_brcond_i64:
        case LIBTCG_INDEX_op_brcond2_i32:
            col += qemu_log("%s$L%d", k ? "," : "", arg_label(args[k])->id);
            i++, k++;
            break;
        default:
            break;
        }
        for (; i < nb_cargs; i++, k++)
        {
            col += qemu_log("%s$0x%" TCG_PRIlx, k ? "," : "", args[k]);
        }
    }
#if 0 // FIXME
    if (op->life)
    {
        unsigned life = op->life;

        for (; col < 48; ++col)
        {
            putc(' ', qemu_logfile);
        }

        if (life & (SYNC_ARG * 3))
        {
            qemu_log("  sync:");
            for (i = 0; i < 2; ++i)
            {
                if (life & (SYNC_ARG << i))
                {
                    qemu_log(" %d", i);
                }
            }
        }
        life /= DEAD_ARG;
        if (life)
        {
            qemu_log("  dead:");
            for (i = 0; life; ++i, life >>= 1)
            {
                if (life & 1)
                {
                    qemu_log(" %d", i);
                }
            }
        }
    }
#endif
    qemu_log("\n");
}
