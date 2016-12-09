
//#include "mkenums.h"
#ifndef MKENUMSTR_INCLUDE_H_
#define MKENUMSTR_INCLUDE_H_


#define STRINGIFY(X) ___STRINGIFY_VIA(X)
/// Via expand macro. No parent
#define ___STRINGIFY_VIA(X) #X


#define MKENUMS_JOIN(A, B) A # B

#if 1 //def MKENUMSTR_COMPILE

enum mkenumstr_oflags_e
{
  O_NODEPS = 1u<<1, // no dependencies on original file or definition
  O_BITFLAGS = 1u<<2,
  O_LSTRIP_COMMON = 1u<<3,
  O_RSTRIP_COMMON = 1u<<4,
  O_JOIN_DUPLS = 1u<<5,
  O_TO_LOWER = 1u<<6,
  O_TO_UPPER = 1u<<7
};

struct mkenumstr_descr_s
{
  const char * enumid;
  const char * resub;
  const char * func;
  const char * file;
  unsigned int oflags;
  unsigned int linenr;
}; /* MKENUMS_JOIN(___mkenums_job_, __LINE__); */


void mkenumstr_hideunused(volatile struct mkenumstr_descr_s * x, void* y)
{}


/*mkenumstr_ofenumIdType -
if enum type and not string, this is a hint to compiler
to have it accesible in symbol table  */

#define MKENUMSTR_FUNC(ENUMID, OFLAGS, RESUB, ...) { \
  static volatile __typeof(ENUMID) mkenumstr_ofenumIdType; \
  static volatile struct mkenumstr_descr_s mkenumstr_job = \
  { \
    .enumid = STRINGIFY(ENUMID), \
    .resub = RESUB, \
    .func = __func__, \
    .file = __FILE__, \
    .oflags = OFLAGS, \
    .linenr = __LINE__ \
  }; /* MKENUMS_JOIN(___mkenums_job_, __LINE__); */ \
  mkenumstr_hideunused(&mkenumstr_job, (void*) &mkenumstr_ofenumIdType);\
  return NULL; \
}

//----- sketch -------------------------------------------
#define MKENUM2STR_FUNC_BITPOS(a,b,c)

#define FUNC(...) FUNC2(__VA_ARGS__, "1", "2", "3")

#define FUNC2(A, B, C, ...) printf("%s %s %s\n", STRINGIFY(A), B, C)

#else

#define MKENUMS_FUNC(id, re, flgs)
#endif /* MKENUMSTR_COMPILE */


#endif /* MKENUMSTR_INCLUDE_H_ */
