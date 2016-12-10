

#ifndef ENUMSTR_INCLUDE_H_
#define ENUMSTR_INCLUDE_H_
#include <wchar.h>
#include "menumstr.h"
#include "testenums.h"

/*
either include all enum defs files or add relative path to sympol table(s)
i.e. .elf or .o

*/

//MKENUMS_INCLUDE("../../master/application/build/bart/ma_app.elf");

//alt 1
//MKENUMS_FUNC("sysState_t", "^sysState_/maState", O_BITFLAGS)
//const char * enumstr_ma_state(unsigned int);


//alt 2 __func__
/*
should also create functions
#define enumstr_ma_state_MAX_LENGTH
*/
const char * enumstr_astate(unsigned int a)
MENUS_VALUE2STR("enum testenum_negjmp_e", 0, "");


const char * enumstr_someflags(unsigned int bitpos)
MENUS_VALUE2STR("enum testenum_flg32_e", 0, "");


// TODO this should need no args, type taken from type
const char * enumstr_myenum(enum testenum_simple_e x)
MENUS_VALUE2STR("", "");


const wchar_t * enumstr_myenumw(enum testenum_negjmp_e x)
MENUS_VALUE2STR(enum testenum_negjmp_e, 0, "A", SUB("B"), SUB(a));


const wchar_t * enumstr_myenumExtraUnusedParams(int x, int y)
MENUS_VALUE2STR(enum testenum_negjmp_e, 0, "");

/*
const char * enumstr_ma_flags(unsigned int bitpos)
_MENUMSTR_PROTOTYPE("sysProtection_flag_t", "^sysState_/maState_", O_BITFLAGS);
*/
//__MKENUMS_FUNC("sysState_t", "^sysState_/maState_", O_BITFLAGS);

//const char * enumstr_simple(unsigned int a) MKENUMS_FUNC(enum myEnum_e);

#endif /* ENUMSTR_INCLUDE_H_ */
