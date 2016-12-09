#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <float.h>
#include <assert.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <stdint.h>
#include <stdio.h>
#include <assert.h>

#include <stdio.h>
#include <stdarg.h>
#include "../menums_utils.h"


enum test_e
{
  test_A = 0,
  test_B = 1,
  test_C = 2,
  test_Z = 0,
};
#if 0
#pragma GCC diagnostic push
//#pragma GCC diagnostic warning "-Wswitch"
//#pragma GCC diagnostic warning "-Wswitch-enum"
#pragma GCC diagnostic error "-Wswitch-enum"
void test_caseErr(void)
{
  //enum test_e v = 0;
  typeof(test_A) v = 0;
  switch(v)
  {
    case test_A: break;
    case test_B: break;
    //case test_C: break;
    /*case test_Z: break; */
    default:     break;;
  }
}
#pragma GCC diagnostic pop
#endif
int test_utils_ctz(void)
{
  uint32_t i;
  int err = 0;
  for (i = 0; i < 32; i++)
  {
    uint32_t mask = 1u << i;

    int ctz32A = __builtin_ctz(mask);
    int ctz32B = MENUMS_BITPOS(mask);
    if (ctz32A != ctz32B)
    {
      printf("Fail: BITPOS. i %u, mask: 0x%u, a: %u, b: %u\n",
              i, mask, ctz32A, ctz32B);
      err++;
    }
  }

  return err;
}

int main()
{
  int err = 0;
  err += test_utils_ctz();

 return err;
}
