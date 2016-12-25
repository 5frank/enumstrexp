
//#include "mkenums.h"
#ifndef MKENUMSTR_INCLUDE_H_
#define MKENUMSTR_INCLUDE_H_

#define MKENUMSTR_STRINGIFY(X) ___MKENUMSTR_STRINGIFY_VIA(X)
/// Via expand macro. No parent
#define ___MKENUMSTR_STRINGIFY_VIA(X) #X

struct mkenumstr_job_s
{
  //const char * enums;

  const char * meta_func;
  const char * meta_file;
  unsigned int meta_line;

  const char * name_strip;
  const char * name_excl;
  unsigned int name_join;
  const char * name_joinsep;
  const char * name_default;

  unsigned int inst_join;
  unsigned int use_bitindex;
};

#define MKENUMSTR(FUNC_NAME, ENUM_TYPE, ...) \
{ \
  static volatile struct mkenumstr_job_s mkenumsstr_job = \
  { \
    .enums = MKENUMSTR_STRINGIFY(ENUM_TYPE), \
    .meta_func = MKENUMSTR_STRINGIFY(FUNC_NAME), \
    .meta_file = __FILE__, \
    .meta_line = __LINE__, \
    __VA_ARGS__ \
 }; \
  return mkenumsstr_job.name_default ? mkenumsstr_job.name_default : "\?\?"; \
}

#endif /* MKENUMSTR_INCLUDE_H_ */
