#include <dlfcn.h>
#include <stdio.h>

enum example_flg_e
{
  example_flg_00 = (1u <<  0),
  example_flg_01 = (1u <<  1),
  example_flg_02 = (1u <<  2),
  example_flg_03 = (1u <<  3),
  example_flg_04 = (1u <<  4),
  example_flg_05 = (1u <<  5),
};
__attribute__((visibility("default")))
static volatile enum example_flg_e xeeenum = 0;

#define ARRAYLEN(array)                                                 \
({                                                                      \
  _Static_assert(!__builtin_types_compatible_p(typeof(array),           \
                                               typeof(&(array)[0])),    \
                "Not an array");                                        \
  sizeof((array)) / sizeof((array)[0]);                                 \
})

__attribute__((visibility("default")))
const char A[] = "Value of A";

__attribute__((visibility("hidden")))
const char B[] = "Value of B";

const char C[] = "Value of C";

int main(int argc, char *argv[])
{
    void * hdl;
    const char *ptr;
    unsigned int i;
    const char * symboi[] = {"example_flg_00", "example_flg_e", "enum example_flg_e", "xeeenum", "A", "B", "C"};
    printf("arraylen: %u\n", ARRAYLEN(symboi));

    hdl = dlopen(NULL, 0);
    for (i = 0; i < ARRAYLEN(symboi); i++) {
        const char * symbname = symboi[i];
        ptr = dlsym(hdl, symbname);
        printf("%s = %s\n", symbname, ptr);
    }
    return 0;
}
