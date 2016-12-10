
//#include "mkenums.h"
#ifndef MKENUMSTR_INCLUDE_H_
#define MKENUMSTR_INCLUDE_H_


#define STRINGIFY(X) ___STRINGIFY_VIA(X)
/// Via expand macro. No parent
#define ___STRINGIFY_VIA(X) #X


#define MKENUMS_JOIN(A, B) A # B

#if 1 //def MKENUMSTR_COMPILE
/*
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
}; */



/*mkenumstr_ofenumIdType -
if enum type and not string, this is a hint to compiler
to have it accesible in symbol table  */
/*
#define MKENUMSTR_FUNC(ENUMID, OFLAGS, RESUB, ...) { \
  static volatile typeof(ENUMID) mkenumstr_ofenumIdType; \
  static volatile struct mkenumstr_descr_s mkenumstr_job = \
  { \
    .enumid = STRINGIFY(ENUMID), \
    .resub = RESUB, \
    .func = __func__, \
    .file = __FILE__, \
    .oflags = OFLAGS, \
    .linenr = __LINE__ \
  }\
  mkenumstr_hideunused(&mkenumstr_job, (void*) &mkenumstr_ofenumIdType);\
  return NULL; \
}
*/
struct mkenumstr_descr_s
{
  const char * enumid;
  const char * lutype;
  const char * func;
  const char * file;
  unsigned int linenr;
  const char * args[8];
}; /* MKENUMS_JOIN(___mkenums_job_, __LINE__); */


void mkenumstr_hideunused(volatile struct mkenumstr_descr_s * x, void* y)
{}




#define ___MENUMS_EXPAND(LUTYPE, ENUMID, A1, A2, A3, A4, A5, A6, A7, A8, ...) \
{ \
  static volatile typeof(ENUMID) mkenumstr_ofenumIdType; \
  static volatile struct mkenumstr_descr_s mkenumstr_job = \
  { \
    .enumid = STRINGIFY(ENUMID), \
    .lutype = LUTYPE, \
    .func = __func__, \
    .file = __FILE__, \
    .linenr = __LINE__, \
    .args = \
    { \
      STRINGIFY(A1), \
      STRINGIFY(A2), \
      STRINGIFY(A3), \
      STRINGIFY(A4), \
      STRINGIFY(A5), \
      STRINGIFY(A6), \
      STRINGIFY(A7), \
      STRINGIFY(A8) \
    } \
  }; /* MKENUMS_JOIN(___mkenums_job_, __LINE__); */ \
  mkenumstr_hideunused(&mkenumstr_job, (void*) &mkenumstr_ofenumIdType);\
  return NULL; \
}

#define MENUS_VAARGS(...)  __VA_ARGS__ "", "", "", "", "", "", "", ""


#define ___MENUS_VALUE2STR(...)  ___MENUMS_EXPAND(\
  "VALUE2STR", \
  __VA_ARGS__ \
  "", "", "", "", "", "", "", "")


#define MENUS_VALUE2STR(...) ___MENUS_VALUE2STR(__VA_ARGS__)

#define MENUS_BITFLAG2STR(...) ___MENUMS_EXPAND(\
  "BITFLAG2STR", \
  __VA_ARGS__ \
  "", "", "", "", "", "", "", "")


#else
// TODO
void * menums_default(int x)
{
  return NULL;
}

#define MENUS_VALUE2STR __attribute__ ((weak, alias("menums_default")));
or
#define MENUS_VALUE2STR { _Static_assert(<something)>...

#endif /* MKENUMSTR_COMPILE */



#endif /* MKENUMSTR_INCLUDE_H_ */
