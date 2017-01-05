
//#include "mkenums.h"
#ifndef MKENUMSTR_INCLUDE_H_
#define MKENUMSTR_INCLUDE_H_


#ifdef MKENUMSTR_COMPILE

#define MKENUMSTR_STRINGIFY(X) ___MKENUMSTR_STRINGIFY_VIA(X)
#define ___MKENUMSTR_STRINGIFY_VIA(X) #X

#define MKENUMSTR_UNIQUE(FUNC_NAME) \
  MKENUMSTR_UNIQUE_PASTE(mkenumstr__, FUNC_NAME)
#define MKENUMSTR_UNIQUE_PASTE(A, B) A ## B

struct mkenumstr_job_s
{
  const char * filename;
  unsigned int fileline;

  const char * find;
  const char * funcname;
  const char * funcprmtype;
  unsigned int funcprmsize;
  
  const char * strstrip;
  const char * exclude;

  unsigned int mergedefs;
  unsigned int usebitpos;
};


#define MKENUMSTR_FUNC(FUNC_NAME, FUNC_PRMT, ...) \
static volatile struct mkenumstr_job_s MKENUMSTR_UNIQUE(__LINE__) = \
{ \
  .funcname    = MKENUMSTR_STRINGIFY(FUNC_NAME), \
  .funcprmtype = MKENUMSTR_STRINGIFY(FUNC_PRMT), \
  .funcprmsize = sizeof(FUNC_PRMT), \
  .filename = __FILE__, \
  .fileline = __LINE__, \
  __VA_ARGS__ \
};

#else /* not MKENUMSTR_COMPILE */

#define ___MKENUMSTR_UNUSED_FUNC(FUNC_NAME) \
  ___MKENUMSTR_UNUSED_FUNC_PASTE(__unused, FUNC_NAME)
#define ___MKENUMSTR_UNUSED_FUNC_PASTE(A,B) A ## B

#define MKENUMSTR_FUNC(FUNC_NAME, FUNC_PRMT, ...) \
  const char * ___MKENUMSTR_UNUSED_FUNC(FUNC_NAME)(FUNC_PRMT)

#endif

#endif /* MKENUMSTR_INCLUDE_H_ */
