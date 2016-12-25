
//#include "mkenums.h"
#ifndef MKENUMSTR_INCLUDE_H_
#define MKENUMSTR_INCLUDE_H_

#define MKENUMSTR_STRINGIFY(X) ___MKENUMSTR_STRINGIFY_VIA(X)
#define ___MKENUMSTR_STRINGIFY_VIA(X) #X

#define EXPAND_LINE(LN) #LN
#define MKENUMSTR_UNIQUE(FUNC_NAME) MKENUMSTR_UNIQUE_PASTE(mkenumstr__, FUNC_NAME)
#define MKENUMSTR_UNIQUE_PASTE(A, B) A ## B

struct mkenumstr_defaults_s
{
  const char * joindupsep;
  const char * nameunknown;
};
struct mkenumstr_job_s
{
  const char * filename;
  unsigned int fileline;

  const char * find;
  const char * funcname;
  const char * funcprmtype;

  const char * strstrip;
  const char * exclude;
  unsigned int joindup;

  unsigned int mergedefs;
  unsigned int usebitpos;
};


#define MKENUMSTR_FUNC(FUNC_NAME, FUNC_PRMT, ...) \
const char * FUNC_NAME(FUNC_PRMT x) { return "\?\?"; }; \
static volatile struct mkenumstr_job_s MKENUMSTR_UNIQUE(FUNC_NAME) = \
{ \
  .funcname = MKENUMSTR_STRINGIFY(FUNC_NAME), \
  .funcprmtype = MKENUMSTR_STRINGIFY(FUNC_PRMT), \
  .filename = __FILE__, \
  .fileline = __LINE__, \
  __VA_ARGS__ \
};


//TODO
#define MKENUMSTR_INCLUDE();
#define MKENUMSTR_DEFAULT_SETTINGS()

#endif /* MKENUMSTR_INCLUDE_H_ */
