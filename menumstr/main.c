#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#include <dlfcn.h>
#include <errno.h>
#include <errno.h>
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
#include "enumstr.h"


static uintptr_t parse_addr(const char* hexstr)
{
  assert(hexstr);
  char *endptr;
  uintptr_t addr = (uintptr_t) strtoul(hexstr, &endptr, 16);
  assert(*endptr == '\0');
  assert(errno == 0);

  return addr;
}


//#define JSON_STR(K,V) printf("\""K"\": %s\n", V)
//#define JSON_STR(K,V) printf("\""K"\": %s\n", V)

static void printJobAtAddr(uintptr_t addr)
{
  struct mkenumstr_descr_s * job;
  job = (struct mkenumstr_descr_s *) (addr);

  printf("{\n");
    printf("  \"addr\": \"0x%X\",\n", (unsigned int) addr);
    if (job->enumid[0] == '"')
    {
      printf("  \"enumid\": %s,\n", job->enumid);
      printf("  \"havetype\": false\n,");
    }
    else
    {
      printf("  \"enumid\": \"%s\"\n,", job->enumid);
      printf("  \"havetype\": true\n,");
      //printf("  \"enumtype\": \"%s\"\n,", job->enumid);
    }
    unsigned int oflags = job->oflags;
    unsigned int msk = 1;
    unsigned int i;
    unsigned int maxbitpos = sizeof(oflags) * 8;
    const char * flgname;
    for (i = 0; i < maxbitpos; i++)
    {
      switch(msk)
      {
        case O_NODEPS:        flgname = "nodeps"; break;
        case O_BITFLAGS:      flgname = "bitflags"; break;
        case O_LSTRIP_COMMON: flgname = "lstrip"; break;
        case O_RSTRIP_COMMON: flgname = "rstrip"; break;
        case O_JOIN_DUPLS:    flgname = "joindupl"; break;
        case O_TO_LOWER:      flgname = "tolower"; break;
        case O_TO_UPPER:      flgname = "toupper"; break;
        default:              flgname = NULL;      break;
      }
      if (flgname)
      {
        printf("  \"%s\": %s,\n", flgname, (msk & oflags) ? "true" : "false");
      }
      msk <<= 1;
    }

    printf("  \"oflags\": %u,\n", job->oflags);
    printf("  \"func\": \"%s\",\n", job->func);
    printf("  \"refmt\": \"%s\",\n", job->resub);
    printf("  \"file\": \"%s\",\n", job->file);
    printf("  \"linenr\": %u\n", job->linenr);
    printf("\n}");
}

int main(int argc, char *argv[])
{

  int i;
  printf("[\n");
  for (i = 1; i < argc; i++)
  {
    uintptr_t addr = parse_addr(argv[i]);
    printJobAtAddr(addr);
    if (i < (argc-1)) printf(",\n");
  }
  printf("\n]\n");
#if 1

//printf("%s = %p\n", "symbname", &mkenumstr_job);



#endif
}
