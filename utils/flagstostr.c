#include <limits.h>
#include <stdint.h>

#define FLAG_SEPARATOR '|'

static char * strappnd(char * restrict dst,
                const char * dstlast,
                const char * restrict src)
{
  const unsigned int maxcpy = dstlast - dst;

  unsigned int i;
  for (i = 0; i < maxcpy && *src != '\0'; ++i)
  {
    *dst++ = *src++;
  }
  //if out of space or no nul term in src, dst == lastdst
  *dst = '\0';

  return dst;
}

struct flagdiff32_s
{
  uint32_t flags;
  uint32_t diffMsk;
  uint32_t diffSet;
  uint32_t diffClr;
};

static void flagdiff_update(struct flagdiff32_s * diff, uint32_t newFlags)
{
  diff->diffMsk = newFlags ^ diff->flags;
  diff->diffSet = diff->diffMsk & newFlags;
  diff->diffClr = diff->diffMsk & diff->flags;
  diff->flags = newFlags;
}

static void flagdiff_reset(struct flagdiff32_s * diff)
{
  memset(diff, 0, sizeof(*diff));
}

int flagstostr(char * dest,
               size_t size,
               const char prefix,
               const char delimiter,
               const char * (*lookupfunc) (unsigned int),
               unsigned int flags)
{
  if (!size || !dest || !lookupfunc)
  {
    return -1;
  }
  char * s = dest;

  if (size < 4)
  {
    *s = '\0';
    return -2;
  }

  const char * dstlast = dest + (size - 3); // -1 as last -1 for separator
  unsigned int bitindex = 0;
  for (;;)
  {
    if (flags & 1u)
    {
      if (prefix)
      {
        *s++ = prefix;
      }
      const char * restrict src = lookupfunc(bitindex);
      if (!src)
      {
        src = "?";
      }

      while(*src != '\0')
      {
        if (s == dstlast)
        {
          *s = '\0';
          return s - dest;
        }
        *s++ = *src++;
      }
    }

    flags >>= 1u;

    if (!flags)
    {
      *s = '\0';
      return s - dest;
    }
    if (delimiter)
    {
      *s++ = delimiter;
    }
    bitindex++;
  }

  return s - dest;
}
