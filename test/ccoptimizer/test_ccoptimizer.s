   1              		.cpu arm7tdmi
   2              		.fpu softvfp
   3              		.eabi_attribute 20, 1	@ Tag_ABI_FP_denormal
   4              		.eabi_attribute 21, 1	@ Tag_ABI_FP_exceptions
   5              		.eabi_attribute 23, 3	@ Tag_ABI_FP_number_model
   6              		.eabi_attribute 24, 1	@ Tag_ABI_align8_needed
   7              		.eabi_attribute 25, 1	@ Tag_ABI_align8_preserved
   8              		.eabi_attribute 26, 1	@ Tag_ABI_enum_size
   9              		.eabi_attribute 30, 2	@ Tag_ABI_optimization_goals
  10              		.eabi_attribute 34, 0	@ Tag_CPU_unaligned_access
  11              		.eabi_attribute 18, 4	@ Tag_ABI_PCS_wchar_t
  12              		.file	"test_ccoptimizer.c"
  13              	@ GNU C (GNU Tools for ARM Embedded Processors) version 4.7.3 20130312 (release) [ARM/embedded-4_7-
  14              	@	compiled by GNU C version 4.3.6, GMP version 4.3.2, MPFR version 2.4.2, MPC version 0.8.1
  15              	@ GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
  16              	@ options passed: 
  17              	@ -iprefix /home/sfrank/Documents/gcc-arm-none-eabi-4.7/bin/../lib/gcc/arm-none-eabi/4.7.3/
  18              	@ -isysroot /home/sfrank/Documents/gcc-arm-none-eabi-4.7/bin/../arm-none-eabi
  19              	@ -D__USES_INITFINI__ test_ccoptimizer.c -g -g -O0 -O3 -std=gnu99
  20              	@ -fverbose-asm
  21              	@ options enabled:  -fauto-inc-dec -fbranch-count-reg -fcaller-saves
  22              	@ -fcombine-stack-adjustments -fcommon -fcompare-elim -fcprop-registers
  23              	@ -fcrossjumping -fcse-follow-jumps -fdebug-types-section -fdefer-pop
  24              	@ -fdelete-null-pointer-checks -fdevirtualize -fdwarf2-cfi-asm
  25              	@ -fearly-inlining -feliminate-unused-debug-types -fexpensive-optimizations
  26              	@ -fforward-propagate -ffunction-cse -fgcse -fgcse-after-reload -fgcse-lm
  27              	@ -fgnu-runtime -fguess-branch-probability -fident -fif-conversion
  28              	@ -fif-conversion2 -findirect-inlining -finline -finline-atomics
  29              	@ -finline-functions -finline-functions-called-once
  30              	@ -finline-small-functions -fipa-cp -fipa-cp-clone -fipa-profile
  31              	@ -fipa-pure-const -fipa-reference -fipa-sra -fira-hoist-pressure
  32              	@ -fira-share-save-slots -fira-share-spill-slots -fivopts
  33              	@ -fkeep-static-consts -fleading-underscore -fmath-errno -fmerge-constants
  34              	@ -fmerge-debug-strings -fmove-loop-invariants -fomit-frame-pointer
  35              	@ -foptimize-register-move -foptimize-sibling-calls -foptimize-strlen
  36              	@ -fpartial-inlining -fpeephole -fpeephole2 -fpredictive-commoning
  37              	@ -fprefetch-loop-arrays -freg-struct-return -fregmove -freorder-blocks
  38              	@ -freorder-functions -frerun-cse-after-loop
  39              	@ -fsched-critical-path-heuristic -fsched-dep-count-heuristic
  40              	@ -fsched-group-heuristic -fsched-interblock -fsched-last-insn-heuristic
  41              	@ -fsched-rank-heuristic -fsched-spec -fsched-spec-insn-heuristic
  42              	@ -fsched-stalled-insns-dep -fschedule-insns -fschedule-insns2
  43              	@ -fsection-anchors -fshow-column -fshrink-wrap -fsigned-zeros
  44              	@ -fsplit-ivs-in-unroller -fsplit-wide-types -fstrict-aliasing
  45              	@ -fstrict-overflow -fstrict-volatile-bitfields -fthread-jumps
  46              	@ -ftoplevel-reorder -ftrapping-math -ftree-bit-ccp -ftree-builtin-call-dce
  47              	@ -ftree-ccp -ftree-ch -ftree-copy-prop -ftree-copyrename -ftree-cselim
  48              	@ -ftree-dce -ftree-dominator-opts -ftree-dse -ftree-forwprop -ftree-fre
  49              	@ -ftree-loop-distribute-patterns -ftree-loop-if-convert -ftree-loop-im
  50              	@ -ftree-loop-ivcanon -ftree-loop-optimize -ftree-parallelize-loops=
  51              	@ -ftree-phiprop -ftree-pre -ftree-pta -ftree-reassoc -ftree-scev-cprop
  52              	@ -ftree-sink -ftree-slp-vectorize -ftree-sra -ftree-switch-conversion
  53              	@ -ftree-tail-merge -ftree-ter -ftree-vect-loop-version -ftree-vectorize
  54              	@ -ftree-vrp -funit-at-a-time -funswitch-loops -fvar-tracking
  55              	@ -fvar-tracking-assignments -fverbose-asm -fzero-initialized-in-bss -marm
  56              	@ -mlittle-endian -msched-prolog -mthumb-interwork
  57              	@ -mvectorize-with-neon-quad
  58              	
  59              		.text
  60              	.Ltext0:
  61              		.cfi_sections	.debug_frame
  62              		.align	2
  63              		.global	test_ccoptimizer_nomacro
  65              	test_ccoptimizer_nomacro:
  66              	.LFB0:
  67              		.file 1 "test_ccoptimizer.c"
   1:test_ccoptimizer.c **** #include <stdint.h>
   2:test_ccoptimizer.c **** #include <stdio.h>
   3:test_ccoptimizer.c **** #include <stddef.h>
   4:test_ccoptimizer.c **** #include <string.h>
   5:test_ccoptimizer.c **** #include <float.h>
   6:test_ccoptimizer.c **** #include <assert.h>
   7:test_ccoptimizer.c **** #include <math.h>
   8:test_ccoptimizer.c **** #include <time.h>
   9:test_ccoptimizer.c **** #include <sys/time.h>
  10:test_ccoptimizer.c **** #include <stdint.h>
  11:test_ccoptimizer.c **** #include <stdio.h>
  12:test_ccoptimizer.c **** #include <assert.h>
  13:test_ccoptimizer.c **** 
  14:test_ccoptimizer.c **** #include <stdio.h>
  15:test_ccoptimizer.c **** #include <stdarg.h>
  16:test_ccoptimizer.c **** #include "../menums_utils.h"
  17:test_ccoptimizer.c **** 
  18:test_ccoptimizer.c **** 
  19:test_ccoptimizer.c **** enum test_ccoflg
  20:test_ccoptimizer.c **** {
  21:test_ccoptimizer.c ****   test_ccoflg_00 = (1u <<  0),
  22:test_ccoptimizer.c ****   test_ccoflg_01 = (1u <<  1),
  23:test_ccoptimizer.c ****   test_ccoflg_02 = (1u <<  2),
  24:test_ccoptimizer.c ****   test_ccoflg_03 = (1u <<  3),
  25:test_ccoptimizer.c ****   test_ccoflg_04 = (1u <<  4),
  26:test_ccoptimizer.c ****   test_ccoflg_05 = (1u <<  5),
  27:test_ccoptimizer.c ****   test_ccoflg_06 = (1u <<  6),
  28:test_ccoptimizer.c ****   test_ccoflg_07 = (1u <<  7),
  29:test_ccoptimizer.c ****   test_ccoflg_08 = (1u <<  8),
  30:test_ccoptimizer.c ****   test_ccoflg_09 = (1u <<  9),
  31:test_ccoptimizer.c ****   test_ccoflg_10 = (1u << 10),
  32:test_ccoptimizer.c ****   test_ccoflg_11 = (1u << 11),
  33:test_ccoptimizer.c ****   test_ccoflg_12 = (1u << 12),
  34:test_ccoptimizer.c ****   test_ccoflg_13 = (1u << 13),
  35:test_ccoptimizer.c ****   test_ccoflg_14 = (1u << 14),
  36:test_ccoptimizer.c ****   test_ccoflg_15 = (1u << 15),
  37:test_ccoptimizer.c ****   test_ccoflg_16 = (1u << 16),
  38:test_ccoptimizer.c ****   test_ccoflg_17 = (1u << 17),
  39:test_ccoptimizer.c ****   test_ccoflg_18 = (1u << 18),
  40:test_ccoptimizer.c ****   test_ccoflg_19 = (1u << 19),
  41:test_ccoptimizer.c ****   test_ccoflg_20 = (1u << 20),
  42:test_ccoptimizer.c ****   test_ccoflg_21 = (1u << 21),
  43:test_ccoptimizer.c ****   test_ccoflg_22 = (1u << 22),
  44:test_ccoptimizer.c ****   test_ccoflg_23 = (1u << 23),
  45:test_ccoptimizer.c ****   test_ccoflg_24 = (1u << 24),
  46:test_ccoptimizer.c ****   test_ccoflg_25 = (1u << 25),
  47:test_ccoptimizer.c ****   test_ccoflg_26 = (1u << 26),
  48:test_ccoptimizer.c ****   test_ccoflg_27 = (1u << 27),
  49:test_ccoptimizer.c ****   test_ccoflg_28 = (1u << 28),
  50:test_ccoptimizer.c ****   test_ccoflg_29 = (1u << 29),
  51:test_ccoptimizer.c ****   test_ccoflg_30 = (1u << 30),
  52:test_ccoptimizer.c ****   test_ccoflg_31 = (1u << 31)
  53:test_ccoptimizer.c **** };
  54:test_ccoptimizer.c **** 
  55:test_ccoptimizer.c **** __attribute__ ((noinline))
  56:test_ccoptimizer.c **** const char * test_ccoptimizer_nomacro(uint32_t flgmask)
  57:test_ccoptimizer.c **** {
  68              		.loc 1 57 0
  69              		.cfi_startproc
  70              		@ Function supports interworking.
  71              		@ args = 0, pretend = 0, frame = 0
  72              		@ frame_needed = 0, uses_anonymous_args = 0
  73              		@ link register save eliminated.
  74              	.LVL0:
  58:test_ccoptimizer.c ****   if (!MENUMS_IS_SINGLE_BIT_SET(flgmask))
  75              		.loc 1 58 0
  76 0000 000050E3 		cmp	r0, #0	@ flgmask
  77 0004 1300000A 		beq	.L44	@,
  78              		.loc 1 58 0 is_stmt 0 discriminator 1
  79 0008 013040E2 		sub	r3, r0, #1	@ tmp139, flgmask,
  80 000c 000013E1 		tst	r3, r0	@ tmp139, flgmask
  81 0010 1000001A 		bne	.L44	@,
  59:test_ccoptimizer.c ****   {
  60:test_ccoptimizer.c ****     return "UNKOWN_MULTI_FLAGS";
  61:test_ccoptimizer.c ****   }
  62:test_ccoptimizer.c ****   switch(flgmask)
  82              		.loc 1 62 0 is_stmt 1
  83 0014 020950E3 		cmp	r0, #32768	@ flgmask,
  84 0018 6700000A 		beq	.L18	@,
  85 001c 0F00009A 		bls	.L47	@,
  86 0020 020550E3 		cmp	r0, #8388608	@ flgmask,
  87 0024 5E00000A 		beq	.L26	@,
  88 0028 1A00009A 		bls	.L48	@,
  89 002c 020350E3 		cmp	r0, #134217728	@ flgmask,
  90 0030 4F00000A 		beq	.L30	@,
  91 0034 4500008A 		bhi	.L41	@,
  92 0038 020450E3 		cmp	r0, #33554432	@ flgmask,
  93 003c 7200000A 		beq	.L28	@,
  94 0040 010350E3 		cmp	r0, #67108864	@ flgmask,
  95 0044 6E00000A 		beq	.L29	@,
  96 0048 010450E3 		cmp	r0, #16777216	@ flgmask,
  97 004c 1A00001A 		bne	.L3	@,
  63:test_ccoptimizer.c ****   {
  64:test_ccoptimizer.c ****     case test_ccoflg_00: return "00";
  65:test_ccoptimizer.c ****     case test_ccoflg_01: return "01";
  66:test_ccoptimizer.c ****     case test_ccoflg_02: return "02";
  67:test_ccoptimizer.c ****     case test_ccoflg_03: return "03";
  68:test_ccoptimizer.c ****     case test_ccoflg_04: return "04";
  69:test_ccoptimizer.c ****     case test_ccoflg_05: return "05";
  70:test_ccoptimizer.c ****     case test_ccoflg_06: return "06";
  71:test_ccoptimizer.c ****     case test_ccoflg_07: return "07";
  72:test_ccoptimizer.c ****     case test_ccoflg_08: return "08";
  73:test_ccoptimizer.c ****     case test_ccoflg_09: return "09";
  74:test_ccoptimizer.c ****     case test_ccoflg_10: return "10";
  75:test_ccoptimizer.c ****     case test_ccoflg_11: return "11";
  76:test_ccoptimizer.c ****     case test_ccoflg_12: return "12";
  77:test_ccoptimizer.c ****     case test_ccoflg_13: return "13";
  78:test_ccoptimizer.c ****     case test_ccoflg_14: return "14";
  79:test_ccoptimizer.c ****     case test_ccoflg_15: return "15";
  80:test_ccoptimizer.c ****     case test_ccoflg_16: return "16";
  81:test_ccoptimizer.c ****     case test_ccoflg_17: return "17";
  82:test_ccoptimizer.c ****     case test_ccoflg_18: return "18";
  83:test_ccoptimizer.c ****     case test_ccoflg_19: return "19";
  84:test_ccoptimizer.c ****     case test_ccoflg_20: return "20";
  85:test_ccoptimizer.c ****     case test_ccoflg_21: return "21";
  86:test_ccoptimizer.c ****     case test_ccoflg_22: return "22";
  87:test_ccoptimizer.c ****     case test_ccoflg_23: return "23";
  88:test_ccoptimizer.c ****     case test_ccoflg_24: return "24";
  98              		.loc 1 88 0
  99 0050 EC019FE5 		ldr	r0, .L51	@ D.5886,
 100              	.LVL1:
 101 0054 1EFF2FE1 		bx	lr	@
 102              	.LVL2:
 103              	.L44:
  60:test_ccoptimizer.c ****     return "UNKOWN_MULTI_FLAGS";
 104              		.loc 1 60 0
 105 0058 E8019FE5 		ldr	r0, .L51+4	@ D.5886,
 106              	.LVL3:
 107 005c 1EFF2FE1 		bx	lr	@
 108              	.LVL4:
 109              	.L47:
  62:test_ccoptimizer.c ****   switch(flgmask)
 110              		.loc 1 62 0
 111 0060 800050E3 		cmp	r0, #128	@ flgmask,
 112 0064 5200000A 		beq	.L10	@,
 113 0068 1500009A 		bls	.L49	@,
 114 006c 020B50E3 		cmp	r0, #2048	@ flgmask,
 115 0070 3D00000A 		beq	.L14	@,
 116 0074 2D00008A 		bhi	.L38	@,
 117 0078 020C50E3 		cmp	r0, #512	@ flgmask,
 118 007c 5200000A 		beq	.L12	@,
 119 0080 010B50E3 		cmp	r0, #1024	@ flgmask,
 120 0084 4E00000A 		beq	.L13	@,
 121 0088 010C50E3 		cmp	r0, #256	@ flgmask,
 122 008c 0A00001A 		bne	.L3	@,
  72:test_ccoptimizer.c ****     case test_ccoflg_08: return "08";
 123              		.loc 1 72 0
 124 0090 B4019FE5 		ldr	r0, .L51+8	@ D.5886,
 125              	.LVL5:
 126 0094 1EFF2FE1 		bx	lr	@
 127              	.LVL6:
 128              	.L48:
  62:test_ccoptimizer.c ****   switch(flgmask)
 129              		.loc 1 62 0
 130 0098 020750E3 		cmp	r0, #524288	@ flgmask,
 131 009c 3E00000A 		beq	.L22	@,
 132 00a0 1A00008A 		bhi	.L40	@,
 133 00a4 020850E3 		cmp	r0, #131072	@ flgmask,
 134 00a8 4F00000A 		beq	.L20	@,
 135 00ac 010750E3 		cmp	r0, #262144	@ flgmask,
 136 00b0 4B00000A 		beq	.L21	@,
 137 00b4 010850E3 		cmp	r0, #65536	@ flgmask,
 138 00b8 3B00000A 		beq	.L50	@,
 139              	.L3:
  89:test_ccoptimizer.c ****     case test_ccoflg_25: return "25";
  90:test_ccoptimizer.c ****     case test_ccoflg_26: return "26";
  91:test_ccoptimizer.c ****     case test_ccoflg_27: return "27";
  92:test_ccoptimizer.c ****     case test_ccoflg_28: return "28";
  93:test_ccoptimizer.c ****     case test_ccoflg_29: return "29";
  94:test_ccoptimizer.c ****     case test_ccoflg_30: return "30";
  95:test_ccoptimizer.c ****     case test_ccoflg_31: return "31";
  96:test_ccoptimizer.c ****     default:             return "-1";
 140              		.loc 1 96 0
 141 00bc 8C019FE5 		ldr	r0, .L51+12	@ D.5886,
 142              	.LVL7:
 143 00c0 1EFF2FE1 		bx	lr	@
 144              	.LVL8:
 145              	.L49:
  62:test_ccoptimizer.c ****   switch(flgmask)
 146              		.loc 1 62 0
 147 00c4 080050E3 		cmp	r0, #8	@ flgmask,
 148 00c8 3100000A 		beq	.L6	@,
 149 00cc 0700008A 		bhi	.L37	@,
 150 00d0 020050E3 		cmp	r0, #2	@ flgmask,
 151 00d4 2C00000A 		beq	.L45	@,
 152 00d8 040050E3 		cmp	r0, #4	@ flgmask,
 153 00dc 2800000A 		beq	.L5	@,
 154 00e0 010050E3 		cmp	r0, #1	@ flgmask,
 155 00e4 F4FFFF1A 		bne	.L3	@,
  64:test_ccoptimizer.c ****     case test_ccoflg_00: return "00";
 156              		.loc 1 64 0
 157 00e8 64019FE5 		ldr	r0, .L51+16	@ D.5886,
 158              	.LVL9:
 159 00ec 1EFF2FE1 		bx	lr	@
 160              	.LVL10:
 161              	.L37:
  62:test_ccoptimizer.c ****   switch(flgmask)
 162              		.loc 1 62 0
 163 00f0 200050E3 		cmp	r0, #32	@ flgmask,
 164 00f4 4000000A 		beq	.L8	@,
 165 00f8 400050E3 		cmp	r0, #64	@ flgmask,
 166 00fc 3C00000A 		beq	.L9	@,
 167 0100 100050E3 		cmp	r0, #16	@ flgmask,
 168 0104 ECFFFF1A 		bne	.L3	@,
  68:test_ccoptimizer.c ****     case test_ccoflg_04: return "04";
 169              		.loc 1 68 0
 170 0108 48019FE5 		ldr	r0, .L51+20	@ D.5886,
 171              	.LVL11:
 172 010c 1EFF2FE1 		bx	lr	@
 173              	.LVL12:
 174              	.L40:
  62:test_ccoptimizer.c ****   switch(flgmask)
 175              		.loc 1 62 0
 176 0110 020650E3 		cmp	r0, #2097152	@ flgmask,
 177 0114 3000000A 		beq	.L24	@,
 178 0118 010550E3 		cmp	r0, #4194304	@ flgmask,
 179 011c 2C00000A 		beq	.L25	@,
 180 0120 010650E3 		cmp	r0, #1048576	@ flgmask,
 181 0124 E4FFFF1A 		bne	.L3	@,
  84:test_ccoptimizer.c ****     case test_ccoflg_20: return "20";
 182              		.loc 1 84 0
 183 0128 2C019FE5 		ldr	r0, .L51+24	@ D.5886,
 184              	.LVL13:
 185 012c 1EFF2FE1 		bx	lr	@
 186              	.LVL14:
 187              	.L38:
  62:test_ccoptimizer.c ****   switch(flgmask)
 188              		.loc 1 62 0
 189 0130 020A50E3 		cmp	r0, #8192	@ flgmask,
 190 0134 3800000A 		beq	.L16	@,
 191 0138 010950E3 		cmp	r0, #16384	@ flgmask,
 192 013c 3400000A 		beq	.L17	@,
 193 0140 010A50E3 		cmp	r0, #4096	@ flgmask,
 194 0144 DCFFFF1A 		bne	.L3	@,
  76:test_ccoptimizer.c ****     case test_ccoflg_12: return "12";
 195              		.loc 1 76 0
 196 0148 10019FE5 		ldr	r0, .L51+28	@ D.5886,
 197              	.LVL15:
 198 014c 1EFF2FE1 		bx	lr	@
 199              	.LVL16:
 200              	.L41:
  62:test_ccoptimizer.c ****   switch(flgmask)
 201              		.loc 1 62 0
 202 0150 020250E3 		cmp	r0, #536870912	@ flgmask,
 203 0154 0800000A 		beq	.L32	@,
 204 0158 3100008A 		bhi	.L42	@,
 205 015c 010250E3 		cmp	r0, #268435456	@ flgmask,
 206 0160 D5FFFF1A 		bne	.L3	@,
  92:test_ccoptimizer.c ****     case test_ccoflg_28: return "28";
 207              		.loc 1 92 0
 208 0164 F8009FE5 		ldr	r0, .L51+32	@ D.5886,
 209              	.LVL17:
 210 0168 1EFF2FE1 		bx	lr	@
 211              	.LVL18:
 212              	.L14:
  75:test_ccoptimizer.c ****     case test_ccoflg_11: return "11";
 213              		.loc 1 75 0
 214 016c F4009FE5 		ldr	r0, .L51+36	@ D.5886,
 215              	.LVL19:
 216 0170 1EFF2FE1 		bx	lr	@
 217              	.LVL20:
 218              	.L30:
  91:test_ccoptimizer.c ****     case test_ccoflg_27: return "27";
 219              		.loc 1 91 0
 220 0174 F0009FE5 		ldr	r0, .L51+40	@ D.5886,
 221              	.LVL21:
 222 0178 1EFF2FE1 		bx	lr	@
 223              	.LVL22:
 224              	.L32:
  93:test_ccoptimizer.c ****     case test_ccoflg_29: return "29";
 225              		.loc 1 93 0
 226 017c EC009FE5 		ldr	r0, .L51+44	@ D.5886,
 227              	.LVL23:
 228 0180 1EFF2FE1 		bx	lr	@
 229              	.LVL24:
 230              	.L5:
  66:test_ccoptimizer.c ****     case test_ccoflg_02: return "02";
 231              		.loc 1 66 0
 232 0184 E8009FE5 		ldr	r0, .L51+48	@ D.5886,
 233              	.LVL25:
 234 0188 1EFF2FE1 		bx	lr	@
 235              	.LVL26:
 236              	.L45:
  65:test_ccoptimizer.c ****     case test_ccoflg_01: return "01";
 237              		.loc 1 65 0
 238 018c E4009FE5 		ldr	r0, .L51+52	@ D.5886,
 239              	.LVL27:
  97:test_ccoptimizer.c ****   }
  98:test_ccoptimizer.c **** }
 240              		.loc 1 98 0
 241 0190 1EFF2FE1 		bx	lr	@
 242              	.LVL28:
 243              	.L6:
  67:test_ccoptimizer.c ****     case test_ccoflg_03: return "03";
 244              		.loc 1 67 0
 245 0194 E0009FE5 		ldr	r0, .L51+56	@ D.5886,
 246              	.LVL29:
 247 0198 1EFF2FE1 		bx	lr	@
 248              	.LVL30:
 249              	.L22:
  83:test_ccoptimizer.c ****     case test_ccoflg_19: return "19";
 250              		.loc 1 83 0
 251 019c DC009FE5 		ldr	r0, .L51+60	@ D.5886,
 252              	.LVL31:
 253 01a0 1EFF2FE1 		bx	lr	@
 254              	.LVL32:
 255              	.L26:
  87:test_ccoptimizer.c ****     case test_ccoflg_23: return "23";
 256              		.loc 1 87 0
 257 01a4 D8009FE5 		ldr	r0, .L51+64	@ D.5886,
 258              	.LVL33:
 259 01a8 1EFF2FE1 		bx	lr	@
 260              	.LVL34:
 261              	.L50:
  80:test_ccoptimizer.c ****     case test_ccoflg_16: return "16";
 262              		.loc 1 80 0
 263 01ac D4009FE5 		ldr	r0, .L51+68	@ D.5886,
 264              	.LVL35:
 265 01b0 1EFF2FE1 		bx	lr	@
 266              	.LVL36:
 267              	.L10:
  71:test_ccoptimizer.c ****     case test_ccoflg_07: return "07";
 268              		.loc 1 71 0
 269 01b4 D0009FE5 		ldr	r0, .L51+72	@ D.5886,
 270              	.LVL37:
 271 01b8 1EFF2FE1 		bx	lr	@
 272              	.LVL38:
 273              	.L18:
  79:test_ccoptimizer.c ****     case test_ccoflg_15: return "15";
 274              		.loc 1 79 0
 275 01bc CC009FE5 		ldr	r0, .L51+76	@ D.5886,
 276              	.LVL39:
 277 01c0 1EFF2FE1 		bx	lr	@
 278              	.LVL40:
 279              	.L13:
  74:test_ccoptimizer.c ****     case test_ccoflg_10: return "10";
 280              		.loc 1 74 0
 281 01c4 C8009FE5 		ldr	r0, .L51+80	@ D.5886,
 282              	.LVL41:
 283 01c8 1EFF2FE1 		bx	lr	@
 284              	.LVL42:
 285              	.L12:
  73:test_ccoptimizer.c ****     case test_ccoflg_09: return "09";
 286              		.loc 1 73 0
 287 01cc C4009FE5 		ldr	r0, .L51+84	@ D.5886,
 288              	.LVL43:
 289 01d0 1EFF2FE1 		bx	lr	@
 290              	.LVL44:
 291              	.L25:
  86:test_ccoptimizer.c ****     case test_ccoflg_22: return "22";
 292              		.loc 1 86 0
 293 01d4 C0009FE5 		ldr	r0, .L51+88	@ D.5886,
 294              	.LVL45:
 295 01d8 1EFF2FE1 		bx	lr	@
 296              	.LVL46:
 297              	.L24:
  85:test_ccoptimizer.c ****     case test_ccoflg_21: return "21";
 298              		.loc 1 85 0
 299 01dc BC009FE5 		ldr	r0, .L51+92	@ D.5886,
 300              	.LVL47:
 301 01e0 1EFF2FE1 		bx	lr	@
 302              	.LVL48:
 303              	.L21:
  82:test_ccoptimizer.c ****     case test_ccoflg_18: return "18";
 304              		.loc 1 82 0
 305 01e4 B8009FE5 		ldr	r0, .L51+96	@ D.5886,
 306              	.LVL49:
 307 01e8 1EFF2FE1 		bx	lr	@
 308              	.LVL50:
 309              	.L20:
  81:test_ccoptimizer.c ****     case test_ccoflg_17: return "17";
 310              		.loc 1 81 0
 311 01ec B4009FE5 		ldr	r0, .L51+100	@ D.5886,
 312              	.LVL51:
 313 01f0 1EFF2FE1 		bx	lr	@
 314              	.LVL52:
 315              	.L9:
  70:test_ccoptimizer.c ****     case test_ccoflg_06: return "06";
 316              		.loc 1 70 0
 317 01f4 B0009FE5 		ldr	r0, .L51+104	@ D.5886,
 318              	.LVL53:
 319 01f8 1EFF2FE1 		bx	lr	@
 320              	.LVL54:
 321              	.L8:
  69:test_ccoptimizer.c ****     case test_ccoflg_05: return "05";
 322              		.loc 1 69 0
 323 01fc AC009FE5 		ldr	r0, .L51+108	@ D.5886,
 324              	.LVL55:
 325 0200 1EFF2FE1 		bx	lr	@
 326              	.LVL56:
 327              	.L29:
  90:test_ccoptimizer.c ****     case test_ccoflg_26: return "26";
 328              		.loc 1 90 0
 329 0204 A8009FE5 		ldr	r0, .L51+112	@ D.5886,
 330              	.LVL57:
 331 0208 1EFF2FE1 		bx	lr	@
 332              	.LVL58:
 333              	.L28:
  89:test_ccoptimizer.c ****     case test_ccoflg_25: return "25";
 334              		.loc 1 89 0
 335 020c A4009FE5 		ldr	r0, .L51+116	@ D.5886,
 336              	.LVL59:
 337 0210 1EFF2FE1 		bx	lr	@
 338              	.LVL60:
 339              	.L17:
  78:test_ccoptimizer.c ****     case test_ccoflg_14: return "14";
 340              		.loc 1 78 0
 341 0214 A0009FE5 		ldr	r0, .L51+120	@ D.5886,
 342              	.LVL61:
 343 0218 1EFF2FE1 		bx	lr	@
 344              	.LVL62:
 345              	.L16:
  77:test_ccoptimizer.c ****     case test_ccoflg_13: return "13";
 346              		.loc 1 77 0
 347 021c 9C009FE5 		ldr	r0, .L51+124	@ D.5886,
 348              	.LVL63:
 349 0220 1EFF2FE1 		bx	lr	@
 350              	.LVL64:
 351              	.L42:
  62:test_ccoptimizer.c ****   switch(flgmask)
 352              		.loc 1 62 0
 353 0224 010150E3 		cmp	r0, #1073741824	@ flgmask,
 354 0228 0300000A 		beq	.L33	@,
 355 022c 020150E3 		cmp	r0, #-2147483648	@ flgmask,
 356 0230 A1FFFF1A 		bne	.L3	@,
  95:test_ccoptimizer.c ****     case test_ccoflg_31: return "31";
 357              		.loc 1 95 0
 358 0234 88009FE5 		ldr	r0, .L51+128	@ D.5886,
 359              	.LVL65:
 360 0238 1EFF2FE1 		bx	lr	@
 361              	.LVL66:
 362              	.L33:
  94:test_ccoptimizer.c ****     case test_ccoflg_30: return "30";
 363              		.loc 1 94 0
 364 023c 84009FE5 		ldr	r0, .L51+132	@ D.5886,
 365              	.LVL67:
 366 0240 1EFF2FE1 		bx	lr	@
 367              	.L52:
 368              		.align	2
 369              	.L51:
 370 0244 74000000 		.word	.LC25
 371 0248 00000000 		.word	.LC0
 372 024c 34000000 		.word	.LC9
 373 0250 94000000 		.word	.LC33
 374 0254 14000000 		.word	.LC1
 375 0258 24000000 		.word	.LC5
 376 025c 64000000 		.word	.LC21
 377 0260 44000000 		.word	.LC13
 378 0264 84000000 		.word	.LC29
 379 0268 40000000 		.word	.LC12
 380 026c 80000000 		.word	.LC28
 381 0270 88000000 		.word	.LC30
 382 0274 1C000000 		.word	.LC3
 383 0278 18000000 		.word	.LC2
 384 027c 20000000 		.word	.LC4
 385 0280 60000000 		.word	.LC20
 386 0284 70000000 		.word	.LC24
 387 0288 54000000 		.word	.LC17
 388 028c 30000000 		.word	.LC8
 389 0290 50000000 		.word	.LC16
 390 0294 3C000000 		.word	.LC11
 391 0298 38000000 		.word	.LC10
 392 029c 6C000000 		.word	.LC23
 393 02a0 68000000 		.word	.LC22
 394 02a4 5C000000 		.word	.LC19
 395 02a8 58000000 		.word	.LC18
 396 02ac 2C000000 		.word	.LC7
 397 02b0 28000000 		.word	.LC6
 398 02b4 7C000000 		.word	.LC27
 399 02b8 78000000 		.word	.LC26
 400 02bc 4C000000 		.word	.LC15
 401 02c0 48000000 		.word	.LC14
 402 02c4 90000000 		.word	.LC32
 403 02c8 8C000000 		.word	.LC31
 404              		.cfi_endproc
 405              	.LFE0:
 407              		.global	__ctzsi2
 408              		.align	2
 409              		.global	test_ccoptimizer_wmacro
 411              	test_ccoptimizer_wmacro:
 412              	.LFB1:
  99:test_ccoptimizer.c **** 
 100:test_ccoptimizer.c **** /*
 101:test_ccoptimizer.c **** switch case in this function should give a jumptable */
 102:test_ccoptimizer.c **** __attribute__ ((noinline))
 103:test_ccoptimizer.c **** const char * test_ccoptimizer_wmacro(uint32_t flgmask)
 104:test_ccoptimizer.c **** {
 413              		.loc 1 104 0
 414              		.cfi_startproc
 415              		@ Function supports interworking.
 416              		@ args = 0, pretend = 0, frame = 0
 417              		@ frame_needed = 0, uses_anonymous_args = 0
 418              	.LVL68:
 419 02cc 08402DE9 		stmfd	sp!, {r3, lr}	@,
 420              	.LCFI0:
 421              		.cfi_def_cfa_offset 8
 422              		.cfi_offset 3, -8
 423              		.cfi_offset 14, -4
 105:test_ccoptimizer.c ****   if (!MENUMS_IS_SINGLE_BIT_SET(flgmask))
 424              		.loc 1 105 0
 425 02d0 003050E2 		subs	r3, r0, #0	@ flgmask, flgmask
 426 02d4 0800000A 		beq	.L56	@,
 427              		.loc 1 105 0 is_stmt 0 discriminator 1
 428 02d8 012043E2 		sub	r2, r3, #1	@ tmp141, flgmask,
 429 02dc 030012E1 		tst	r2, r3	@ tmp141, flgmask
 430 02e0 0500001A 		bne	.L56	@,
 106:test_ccoptimizer.c ****   {
 107:test_ccoptimizer.c ****     return "UNKOWN_MULTI_FLAGS";
 108:test_ccoptimizer.c ****   }
 109:test_ccoptimizer.c ****   uint32_t ctz = __builtin_ctz(flgmask);
 431              		.loc 1 109 0 is_stmt 1
 432 02e4 FEFFFFEB 		bl	__ctzsi2	@
 433              	.LVL69:
 434 02e8 1F0050E3 		cmp	r0, #31	@ tmp143,
 435 02ec 0500008A 		bhi	.L57	@,
 436 02f0 18309FE5 		ldr	r3, .L58	@ tmp144,
 437 02f4 000193E7 		ldr	r0, [r3, r0, asl #2]	@ D.5878, CSWTCH.5
 438              	.LVL70:
 439 02f8 000000EA 		b	.L54	@
 440              	.LVL71:
 441              	.L56:
 107:test_ccoptimizer.c ****     return "UNKOWN_MULTI_FLAGS";
 442              		.loc 1 107 0
 443 02fc 10009FE5 		ldr	r0, .L58+4	@ D.5878,
 444              	.LVL72:
 445              	.L54:
 110:test_ccoptimizer.c ****   switch(ctz)
 111:test_ccoptimizer.c ****   {
 112:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_00): return "00";
 113:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_01): return "01";
 114:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_02): return "02";
 115:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_03): return "03";
 116:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_04): return "04";
 117:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_05): return "05";
 118:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_06): return "06";
 119:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_07): return "07";
 120:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_08): return "08";
 121:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_09): return "09";
 122:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_10): return "10";
 123:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_11): return "11";
 124:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_12): return "12";
 125:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_13): return "13";
 126:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_14): return "14";
 127:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_15): return "15";
 128:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_16): return "16";
 129:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_17): return "17";
 130:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_18): return "18";
 131:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_19): return "19";
 132:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_20): return "20";
 133:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_21): return "21";
 134:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_22): return "22";
 135:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_23): return "23";
 136:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_24): return "24";
 137:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_25): return "25";
 138:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_26): return "26";
 139:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_27): return "27";
 140:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_28): return "28";
 141:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_29): return "29";
 142:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_30): return "30";
 143:test_ccoptimizer.c ****     case MENUMS_CTZ32(test_ccoflg_31): return "31";
 144:test_ccoptimizer.c ****     default:                           return "-1";
 145:test_ccoptimizer.c ****   }
 146:test_ccoptimizer.c **** }
 446              		.loc 1 146 0
 447 0300 0840BDE8 		ldmfd	sp!, {r3, lr}
 448 0304 1EFF2FE1 		bx	lr
 449              	.LVL73:
 450              	.L57:
 109:test_ccoptimizer.c ****   uint32_t ctz = __builtin_ctz(flgmask);
 451              		.loc 1 109 0
 452 0308 08009FE5 		ldr	r0, .L58+8	@ D.5878,
 453              	.LVL74:
 454 030c FBFFFFEA 		b	.L54	@
 455              	.L59:
 456              		.align	2
 457              	.L58:
 458 0310 00000000 		.word	.LANCHOR0
 459 0314 00000000 		.word	.LC0
 460 0318 94000000 		.word	.LC33
 461              		.cfi_endproc
 462              	.LFE1:
 464              		.section	.text.startup,"ax",%progbits
 465              		.align	2
 466              		.global	main
 468              	main:
 469              	.LFB2:
 147:test_ccoptimizer.c **** 
 148:test_ccoptimizer.c **** int main()
 149:test_ccoptimizer.c **** {
 470              		.loc 1 149 0
 471              		.cfi_startproc
 472              		@ Function supports interworking.
 473              		@ args = 0, pretend = 0, frame = 8
 474              		@ frame_needed = 0, uses_anonymous_args = 0
 475 0000 04E02DE5 		str	lr, [sp, #-4]!	@,
 476              	.LCFI1:
 477              		.cfi_def_cfa_offset 4
 478              		.cfi_offset 14, -4
 150:test_ccoptimizer.c ****   volatile uint32_t flgmask = 1u << 3;
 479              		.loc 1 150 0
 480 0004 0830A0E3 		mov	r3, #8	@ tmp139,
 149:test_ccoptimizer.c **** {
 481              		.loc 1 149 0
 482 0008 0CD04DE2 		sub	sp, sp, #12	@,,
 483              	.LCFI2:
 484              		.cfi_def_cfa_offset 16
 485              		.loc 1 150 0
 486 000c 04308DE5 		str	r3, [sp, #4]	@ tmp139, flgmask
 487              	.LVL75:
 151:test_ccoptimizer.c ****   printf("%s\n", test_ccoptimizer_wmacro(flgmask));
 488              		.loc 1 151 0
 489 0010 04009DE5 		ldr	r0, [sp, #4]	@ flgmask.0, flgmask
 490 0014 FEFFFFEB 		bl	test_ccoptimizer_wmacro	@
 491              	.LVL76:
 492 0018 FEFFFFEB 		bl	puts	@
 493              	.LVL77:
 152:test_ccoptimizer.c ****   printf("%s\n", test_ccoptimizer_nomacro(flgmask));
 494              		.loc 1 152 0
 495 001c 04009DE5 		ldr	r0, [sp, #4]	@ flgmask.1, flgmask
 496 0020 FEFFFFEB 		bl	test_ccoptimizer_nomacro	@
 497              	.LVL78:
 498 0024 FEFFFFEB 		bl	puts	@
 499              	.LVL79:
 153:test_ccoptimizer.c **** 
 154:test_ccoptimizer.c ****  return 0;
 155:test_ccoptimizer.c **** }
 500              		.loc 1 155 0
 501 0028 0000A0E3 		mov	r0, #0	@,
 502 002c 0CD08DE2 		add	sp, sp, #12	@,,
 503 0030 04E09DE4 		ldr	lr, [sp], #4
 504 0034 1EFF2FE1 		bx	lr
 505              		.cfi_endproc
 506              	.LFE2:
 508              		.section	.rodata
 509              		.align	2
 510              		.set	.LANCHOR0,. + 0
 513              	CSWTCH.5:
 514 0000 14000000 		.word	.LC1
 515 0004 18000000 		.word	.LC2
 516 0008 1C000000 		.word	.LC3
 517 000c 20000000 		.word	.LC4
 518 0010 24000000 		.word	.LC5
 519 0014 28000000 		.word	.LC6
 520 0018 2C000000 		.word	.LC7
 521 001c 30000000 		.word	.LC8
 522 0020 34000000 		.word	.LC9
 523 0024 38000000 		.word	.LC10
 524 0028 3C000000 		.word	.LC11
 525 002c 40000000 		.word	.LC12
 526 0030 44000000 		.word	.LC13
 527 0034 48000000 		.word	.LC14
 528 0038 4C000000 		.word	.LC15
 529 003c 50000000 		.word	.LC16
 530 0040 54000000 		.word	.LC17
 531 0044 58000000 		.word	.LC18
 532 0048 5C000000 		.word	.LC19
 533 004c 60000000 		.word	.LC20
 534 0050 64000000 		.word	.LC21
 535 0054 68000000 		.word	.LC22
 536 0058 6C000000 		.word	.LC23
 537 005c 70000000 		.word	.LC24
 538 0060 74000000 		.word	.LC25
 539 0064 78000000 		.word	.LC26
 540 0068 7C000000 		.word	.LC27
 541 006c 80000000 		.word	.LC28
 542 0070 84000000 		.word	.LC29
 543 0074 88000000 		.word	.LC30
 544 0078 8C000000 		.word	.LC31
 545 007c 90000000 		.word	.LC32
 546              		.section	.rodata.str1.4,"aMS",%progbits,1
 547              		.align	2
 548              	.LC0:
 549 0000 554E4B4F 		.ascii	"UNKOWN_MULTI_FLAGS\000"
 549      574E5F4D 
 549      554C5449 
 549      5F464C41 
 549      475300
 550 0013 00       		.space	1
 551              	.LC1:
 552 0014 303000   		.ascii	"00\000"
 553 0017 00       		.space	1
 554              	.LC2:
 555 0018 303100   		.ascii	"01\000"
 556 001b 00       		.space	1
 557              	.LC3:
 558 001c 303200   		.ascii	"02\000"
 559 001f 00       		.space	1
 560              	.LC4:
 561 0020 303300   		.ascii	"03\000"
 562 0023 00       		.space	1
 563              	.LC5:
 564 0024 303400   		.ascii	"04\000"
 565 0027 00       		.space	1
 566              	.LC6:
 567 0028 303500   		.ascii	"05\000"
 568 002b 00       		.space	1
 569              	.LC7:
 570 002c 303600   		.ascii	"06\000"
 571 002f 00       		.space	1
 572              	.LC8:
 573 0030 303700   		.ascii	"07\000"
 574 0033 00       		.space	1
 575              	.LC9:
 576 0034 303800   		.ascii	"08\000"
 577 0037 00       		.space	1
 578              	.LC10:
 579 0038 303900   		.ascii	"09\000"
 580 003b 00       		.space	1
 581              	.LC11:
 582 003c 313000   		.ascii	"10\000"
 583 003f 00       		.space	1
 584              	.LC12:
 585 0040 313100   		.ascii	"11\000"
 586 0043 00       		.space	1
 587              	.LC13:
 588 0044 313200   		.ascii	"12\000"
 589 0047 00       		.space	1
 590              	.LC14:
 591 0048 313300   		.ascii	"13\000"
 592 004b 00       		.space	1
 593              	.LC15:
 594 004c 313400   		.ascii	"14\000"
 595 004f 00       		.space	1
 596              	.LC16:
 597 0050 313500   		.ascii	"15\000"
 598 0053 00       		.space	1
 599              	.LC17:
 600 0054 313600   		.ascii	"16\000"
 601 0057 00       		.space	1
 602              	.LC18:
 603 0058 313700   		.ascii	"17\000"
 604 005b 00       		.space	1
 605              	.LC19:
 606 005c 313800   		.ascii	"18\000"
 607 005f 00       		.space	1
 608              	.LC20:
 609 0060 313900   		.ascii	"19\000"
 610 0063 00       		.space	1
 611              	.LC21:
 612 0064 323000   		.ascii	"20\000"
 613 0067 00       		.space	1
 614              	.LC22:
 615 0068 323100   		.ascii	"21\000"
 616 006b 00       		.space	1
 617              	.LC23:
 618 006c 323200   		.ascii	"22\000"
 619 006f 00       		.space	1
 620              	.LC24:
 621 0070 323300   		.ascii	"23\000"
 622 0073 00       		.space	1
 623              	.LC25:
 624 0074 323400   		.ascii	"24\000"
 625 0077 00       		.space	1
 626              	.LC26:
 627 0078 323500   		.ascii	"25\000"
 628 007b 00       		.space	1
 629              	.LC27:
 630 007c 323600   		.ascii	"26\000"
 631 007f 00       		.space	1
 632              	.LC28:
 633 0080 323700   		.ascii	"27\000"
 634 0083 00       		.space	1
 635              	.LC29:
 636 0084 323800   		.ascii	"28\000"
 637 0087 00       		.space	1
 638              	.LC30:
 639 0088 323900   		.ascii	"29\000"
 640 008b 00       		.space	1
 641              	.LC31:
 642 008c 333000   		.ascii	"30\000"
 643 008f 00       		.space	1
 644              	.LC32:
 645 0090 333100   		.ascii	"31\000"
 646 0093 00       		.space	1
 647              	.LC33:
 648 0094 2D3100   		.ascii	"-1\000"
 649 0097 00       		.text
 650              	.Letext0:
 651              		.file 2 "/home/sfrank/Documents/gcc-arm-none-eabi-4.7/bin/../lib/gcc/arm-none-eabi/4.7.3/../../../
 652              		.file 3 "<built-in>"
