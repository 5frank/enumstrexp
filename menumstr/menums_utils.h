#ifndef MENUMS_UTILS_INCLUDE_H_
#define MENUMS_UTILS_INCLUDE_H_

/// multi evaluation macro. use with care
#define MENUMS_IS_SINGLE_BIT_SET(V) ((V) && !((V) & ((V) - 1)))

#define MENUMS_ASSERT_SINGLE_BIT_SET(V) \
  _Static_assert((V) && !((V) & ((V) - 1)), \
               "Value have more then one bit set (or equals zero)")

 /**
 The botpos macros also ensure single bit set
 */
/** Bit Mask Compare */
#define ___MSKCMP(X, POS) ((X) == (1u << POS)) ? POS :

/// Should fit in uint8 but not conflict with uint128 max bit pos (127)
#define MENUMS_BITPOS_ERROR (-1)

#define MENUMS_BITPOS32(X) ( \
  ___MSKCMP(X,  0) ___MSKCMP(X,  1) ___MSKCMP(X,  2) ___MSKCMP(X,  3) \
  ___MSKCMP(X,  4) ___MSKCMP(X,  5) ___MSKCMP(X,  6) ___MSKCMP(X,  7) \
  ___MSKCMP(X,  8) ___MSKCMP(X,  9) ___MSKCMP(X, 10) ___MSKCMP(X, 11) \
  ___MSKCMP(X, 12) ___MSKCMP(X, 13) ___MSKCMP(X, 14) ___MSKCMP(X, 15) \
  ___MSKCMP(X, 16) ___MSKCMP(X, 17) ___MSKCMP(X, 18) ___MSKCMP(X, 19) \
  ___MSKCMP(X, 20) ___MSKCMP(X, 21) ___MSKCMP(X, 22) ___MSKCMP(X, 23) \
  ___MSKCMP(X, 24) ___MSKCMP(X, 25) ___MSKCMP(X, 26) ___MSKCMP(X, 27) \
  ___MSKCMP(X, 28) ___MSKCMP(X, 29) ___MSKCMP(X, 30) ___MSKCMP(X, 31) \
  MENUMS_BITPOS_ERROR)

/* ensure single bit set or 'duplicate case value' -
  assuming case ENUMSTR_BAD_FLAG_VAL: handled as default */
#define MENUMS_BITPOS64(X) ( \
  ___MSKCMP(X,  0) ___MSKCMP(X,  1) ___MSKCMP(X,  2) ___MSKCMP(X,  3) \
  ___MSKCMP(X,  4) ___MSKCMP(X,  5) ___MSKCMP(X,  6) ___MSKCMP(X,  7) \
  ___MSKCMP(X,  8) ___MSKCMP(X,  9) ___MSKCMP(X, 10) ___MSKCMP(X, 11) \
  ___MSKCMP(X, 12) ___MSKCMP(X, 13) ___MSKCMP(X, 14) ___MSKCMP(X, 15) \
  ___MSKCMP(X, 16) ___MSKCMP(X, 17) ___MSKCMP(X, 18) ___MSKCMP(X, 19) \
  ___MSKCMP(X, 20) ___MSKCMP(X, 21) ___MSKCMP(X, 22) ___MSKCMP(X, 23) \
  ___MSKCMP(X, 24) ___MSKCMP(X, 25) ___MSKCMP(X, 26) ___MSKCMP(X, 27) \
  ___MSKCMP(X, 28) ___MSKCMP(X, 29) ___MSKCMP(X, 30) ___MSKCMP(X, 31) \
  ___MSKCMP(X, 32) ___MSKCMP(X, 33) ___MSKCMP(X, 34) ___MSKCMP(X, 35) \
  ___MSKCMP(X, 36) ___MSKCMP(X, 37) ___MSKCMP(X, 38) ___MSKCMP(X, 39) \
  ___MSKCMP(X, 40) ___MSKCMP(X, 41) ___MSKCMP(X, 42) ___MSKCMP(X, 43) \
  ___MSKCMP(X, 44) ___MSKCMP(X, 45) ___MSKCMP(X, 46) ___MSKCMP(X, 47) \
  ___MSKCMP(X, 48) ___MSKCMP(X, 49) ___MSKCMP(X, 50) ___MSKCMP(X, 51) \
  ___MSKCMP(X, 52) ___MSKCMP(X, 53) ___MSKCMP(X, 54) ___MSKCMP(X, 55) \
  ___MSKCMP(X, 56) ___MSKCMP(X, 57) ___MSKCMP(X, 58) ___MSKCMP(X, 59) \
  ___MSKCMP(X, 60) ___MSKCMP(X, 61) ___MSKCMP(X, 62) ___MSKCMP(X, 63) \
  MENUMS_BITPOS_ERROR)

#define MENUMS_BITPOS(X) MENUMS_BITPOS32(X)
/*
#define MENUMS_CC_ERROR_MISSING_ENUM_CASE_ENABLE() \
  _Pragma("GCC diagnostic push") \
  _Pragma("GCC diagnostic error \"-Wswitch-enum\"")\
#pragma GCC diagnostic push
//#pragma GCC diagnostic warning "-Wswitch"
//#pragma GCC diagnostic warning "-Wswitch-enum"
#pragma GCC diagnostic error "-Wswitch-enum"
*/


typedef const char * (*menums_bftostrluf) (unsigned int bitpos);

#define MENUMS_STR_SIZE_MAX(FUNC) FUNC #

ssize_t menums_bitstostr(char * str, size_t size, unit32_t flags);
ssize_t menums_bitstostr(char * str, size_t size, unsigned int flags, menums_bftostrluf)
{
  size_t w
  unsigned int i = 0;
  while (flags)
  {
#if 1
    // undefined result if param is 0
    unsigned int bp = (unsigned int) __builtin_ctz(flags);
    flags &= ~(1u << bp);
#endif
    if (flags & 1u])
    {
      wrsize += strappend(str, *menums_bftostrluf(i);
    }
    flags >>= 1u; // can aussume logical shift as unsigned type
    return 0;
  }

  unsigned int ___flgs = (FLAGS);
  for (i = 0; i < (sizeof(flgs) * CHAR_BIT); i++)
}


#include <limit.h>
#define ENUMSTR_FLGS(STRBUF, TOSTREXPR, FLAGS) \
({
  char * ___buf = (STRBUF);
  unsigned typeof(FLAGS) ___flgs = (FLAGS);
  unsigned int ___i;
  for (___i = 0; ___i < (sizeof(___flgs) * CHAR_BIT); ___i++)
  {
    if (__i
    strappend(S
  }
#endif /* MENUMS_UTILS_INCLUDE_H_ */
