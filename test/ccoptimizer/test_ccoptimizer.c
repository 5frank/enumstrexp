#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <float.h>
#include <assert.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <stdint.h>
#include <stdio.h>
#include <assert.h>

#include <stdio.h>
#include <stdarg.h>
#include "../menums_utils.h"

enum test_ccoflg
{
  test_ccoflg_00 = (1u <<  0),
  test_ccoflg_01 = (1u <<  1),
  test_ccoflg_02 = (1u <<  2),
  test_ccoflg_03 = (1u <<  3),
  test_ccoflg_04 = (1u <<  4),
  test_ccoflg_05 = (1u <<  5),
  test_ccoflg_06 = (1u <<  6),
  test_ccoflg_07 = (1u <<  7),
  test_ccoflg_08 = (1u <<  8),
  test_ccoflg_09 = (1u <<  9),
  test_ccoflg_10 = (1u << 10),
  test_ccoflg_11 = (1u << 11),
  test_ccoflg_12 = (1u << 12),
  test_ccoflg_13 = (1u << 13),
  test_ccoflg_14 = (1u << 14),
  test_ccoflg_15 = (1u << 15),
  test_ccoflg_16 = (1u << 16),
  test_ccoflg_17 = (1u << 17),
  test_ccoflg_18 = (1u << 18),
  test_ccoflg_19 = (1u << 19),
  test_ccoflg_20 = (1u << 20),
  test_ccoflg_21 = (1u << 21),
  test_ccoflg_22 = (1u << 22),
  test_ccoflg_23 = (1u << 23),
  test_ccoflg_24 = (1u << 24),
  test_ccoflg_25 = (1u << 25),
  test_ccoflg_26 = (1u << 26),
  test_ccoflg_27 = (1u << 27),
  test_ccoflg_28 = (1u << 28),
  test_ccoflg_29 = (1u << 29),
  test_ccoflg_30 = (1u << 30),
  test_ccoflg_31 = (1u << 31)
};

/*
no jumptable. gcc does not seem to see the obvious pattern here.
i.e. use shitf t */
__attribute__ ((noinline))
const char * test_ccoptimizer_nomacro(uint32_t flgmask)
{
  if (!MENUMS_IS_SINGLE_BIT_SET(flgmask))
  {
    return "UNKOWN_MULTI_FLAGS";
  }
  switch(flgmask)
  {
    case test_ccoflg_00: return "00";
    case test_ccoflg_01: return "01";
    case test_ccoflg_02: return "02";
    case test_ccoflg_03: return "03";
    case test_ccoflg_04: return "04";
    case test_ccoflg_05: return "05";
    case test_ccoflg_06: return "06";
    case test_ccoflg_07: return "07";
    case test_ccoflg_08: return "08";
    case test_ccoflg_09: return "09";
    case test_ccoflg_10: return "10";
    case test_ccoflg_11: return "11";
    case test_ccoflg_12: return "12";
    case test_ccoflg_13: return "13";
    case test_ccoflg_14: return "14";
    case test_ccoflg_15: return "15";
    case test_ccoflg_16: return "16";
    case test_ccoflg_17: return "17";
    case test_ccoflg_18: return "18";
    case test_ccoflg_19: return "19";
    case test_ccoflg_20: return "20";
    case test_ccoflg_21: return "21";
    case test_ccoflg_22: return "22";
    case test_ccoflg_23: return "23";
    case test_ccoflg_24: return "24";
    case test_ccoflg_25: return "25";
    case test_ccoflg_26: return "26";
    case test_ccoflg_27: return "27";
    case test_ccoflg_28: return "28";
    case test_ccoflg_29: return "29";
    case test_ccoflg_30: return "30";
    case test_ccoflg_31: return "31";
    default:             return "-1";
  }
}

/*
switch case in this function should give a jumptable */
__attribute__ ((noinline))
const char * test_ccoptimizer_wmacro(uint32_t flgmask)
{
  if (!MENUMS_IS_SINGLE_BIT_SET(flgmask))
  {
    return "<UNKOWN>";
  }
  uint32_t ctz = __builtin_ctz(flgmask);
  switch(ctz)
  {
    case MENUMS_CTZ32(test_ccoflg_00): return "00";
    case MENUMS_CTZ32(test_ccoflg_01): return "01";
    case MENUMS_CTZ32(test_ccoflg_02): return "02";
    case MENUMS_CTZ32(test_ccoflg_03): return "03";
    case MENUMS_CTZ32(test_ccoflg_04): return "04";
    case MENUMS_CTZ32(test_ccoflg_05): return "05";
    case MENUMS_CTZ32(test_ccoflg_06): return "06";
    case MENUMS_CTZ32(test_ccoflg_07): return "07";
    case MENUMS_CTZ32(test_ccoflg_08): return "08";
    case MENUMS_CTZ32(test_ccoflg_09): return "09";
    case MENUMS_CTZ32(test_ccoflg_10): return "10";
    case MENUMS_CTZ32(test_ccoflg_11): return "11";
    case MENUMS_CTZ32(test_ccoflg_12): return "12";
    case MENUMS_CTZ32(test_ccoflg_13): return "13";
    case MENUMS_CTZ32(test_ccoflg_14): return "14";
    case MENUMS_CTZ32(test_ccoflg_15): return "15";
    case MENUMS_CTZ32(test_ccoflg_16): return "16";
    case MENUMS_CTZ32(test_ccoflg_17): return "17";
    case MENUMS_CTZ32(test_ccoflg_18): return "18";
    case MENUMS_CTZ32(test_ccoflg_19): return "19";
    case MENUMS_CTZ32(test_ccoflg_20): return "20";
    case MENUMS_CTZ32(test_ccoflg_21): return "21";
    case MENUMS_CTZ32(test_ccoflg_22): return "22";
    case MENUMS_CTZ32(test_ccoflg_23): return "23";
    case MENUMS_CTZ32(test_ccoflg_24): return "24";
    case MENUMS_CTZ32(test_ccoflg_25): return "25";
    case MENUMS_CTZ32(test_ccoflg_26): return "26";
    case MENUMS_CTZ32(test_ccoflg_27): return "27";
    case MENUMS_CTZ32(test_ccoflg_28): return "28";
    case MENUMS_CTZ32(test_ccoflg_29): return "29";
    case MENUMS_CTZ32(test_ccoflg_30): return "30";
    case MENUMS_CTZ32(test_ccoflg_31): return "31";
    default:                           return "<UNKOWN>";
  }
}

int main()
{
  volatile uint32_t flgmask = 1u << 3;
  printf("%s\n", test_ccoptimizer_wmacro(flgmask));
  printf("%s\n", test_ccoptimizer_nomacro(flgmask));

 return 0;
}
