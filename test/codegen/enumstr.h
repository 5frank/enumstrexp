

#ifndef ENUMSTR_INCLUDE_H_
#define ENUMSTR_INCLUDE_H_
#include <stdint.h>
#include <stdbool.h>

#include <mkenumstr.h>
#include "../testdefs.h"

#ifndef MKENUMSTR_COMPILE
#error "undef wtf?"
#endif


MKENUMSTR_FUNC(enumstr_myenum0, enum testenum_negjmp_e);


MKENUMSTR_FUNC(enumstr_myenum1, enum testenum_negjmp_e,
  .strstrip="^testenum_negjmp_", .exclude="_LAST");


MKENUMSTR_FUNC(enumstr_myenum2, int,
  .find="enum testenum_negjmp_");

#if 0
MKENUMSTR_FUNC(enumstr_myenum3, int,
    .find = "^syserr_*",
    .exclude = "^_",
    .strstrip = "^syserr_",
    .mergedefs = true
);

MKENUMSTR_FUNC(enumstr_myenum3, int, "^syserr_*",
    .name_excl = "^_",
    .name_strip = "^syserr_",
    .defs_merge = true
);
#endif

#endif /* ENUMSTR_INCLUDE_H_ */
