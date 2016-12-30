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

int flagstostr(char * dest,
               size_t size,
               const char * (*lookupfunc) (unsigned int),
               unsigned int flags)
{
  if (!dest || !lookupfunc)
  {
    return -1;
  }
  if (!size)
  {
    return -2;
  }
  char * s = dest;
  const char * dstlast = s + (size - 2); // -1 as last -1 for separator
  unsigned int i = 0;
  for (i = 0; i < (sizeof(flags) * CHAR_BIT); i++)
  {
    if (flags & 1u)
    {
      s = strappnd(s, dstlast, lookupfunc(i));
      if (s == dstlast)
      {
        break;
      }
    }

    flags >>= 1u;

    if (flags)
    {
      *s++ = FLAG_SEPARATOR;
    }
    else
    {
      break;
    }
  }

  return s - dest;
}
