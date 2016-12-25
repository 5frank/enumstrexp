
//#include "mkenums.h"
#ifndef MKENUMSTR_INCLUDE_H_
#define MKENUMSTR_INCLUDE_H_

#define MKENUMSTR_STRINGIFY(X) ___MKENUMSTR_STRINGIFY_VIA(X)
#define ___MKENUMSTR_STRINGIFY_VIA(X) #X

#define EXPAND_LINE(LN) #LN
#define MKENUMSTR_UNIQUE(FUNC_NAME) MKENUMSTR_UNIQUE_PASTE(mkenumstr__, FUNC_NAME)
#define MKENUMSTR_UNIQUE_PASTE(A, B) A ## B

struct mkenumstr_job_s
{
  const char * meta_file;
  unsigned int meta_line;

  const char * func_name;
  const char * func_prmt;
  const char * find_expr;

  const char * name_strip;
  const char * name_excl;
  unsigned int name_join;
  const char * name_joinsep;
  const char * name_default;

  unsigned int defs_merge;
  unsigned int use_bitindex;
};


#define MKENUMSTR_FUNC(FUNC_NAME, FUNC_PRMT, ...) \
const char * FUNC_NAME(FUNC_PRMT x) { return "\?\?"; }; \
static volatile struct mkenumstr_job_s MKENUMSTR_UNIQUE(FUNC_NAME) = \
{ \
  .func_name = MKENUMSTR_STRINGIFY(FUNC_NAME), \
  .func_prmt = MKENUMSTR_STRINGIFY(FUNC_PRMT), \
  .meta_file = __FILE__, \
  .meta_line = __LINE__, \
  __VA_ARGS__ \
};


//TODO
#define MKENUMSTR_INCLUDE();
#define MKENUMSTR_DEFAULT_SETTINGS()

#endif /* MKENUMSTR_INCLUDE_H_ */
