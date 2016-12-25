

#ifndef ENUMSTR_INCLUDE_H_
#define ENUMSTR_INCLUDE_H_
#include <stdint.h>
#include <stdbool.h>

#include <mkenumstr.h>
#include "../testenums.h"

#ifndef MKENUMSTR_COMPILE
#error "undef wtf?"
#endif


MKENUMSTR_FUNC(enumstr_myenum1, enum testenum_negjmp_e);

#if 0
MKENUMSTR(enumstr_myenum3, int,
    .find_expr="^syserr_*",
    .name_excl = "^_",
    .name_strip = "^syserr_",
    .defs_merge = true
);

MKENUMSTR(enumstr_myenum3, int, "^syserr_*",
    .name_excl = "^_",
    .name_strip = "^syserr_",
    .defs_merge = true
);
#endif

#endif /* ENUMSTR_INCLUDE_H_ */
