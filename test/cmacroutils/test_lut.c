
// Print a leading + or - if the flag was set or cleared.
// This is not done if no flags were set previously.

static size_t menums_flagDiff(char * dst,
                              size_t size,
                              uint32_t newflags,
                              uint32_t oldflags)
{
  size_t wrCnt  = 0;
  uint32_t mask = 1;
  uint32_t changedflags = newflags ^ oldflags;
  char prefix = ' ';
  dst[0] = '\0'; // if nothing new, clear old

  uint32_t i; // bit position
  for (i = 0; i < 32; i++)
  {
    if (mask & changedflags)
    {
      if (oldflags != 0) //
      {
        if (mask & newflags)
        { prefix = '+'; }
        else
        { prefix = '-'; }
      }
      else // no flags were set previously
      {
        prefix = ' ';
      }
      int r = snprintf(&dst[wrCnt], size - wrCnt, "%c%s ", prefix, enumstr_sfFlag(i));
      wrCnt += (r > 0) ? (size_t)r : 0; // dont add  negatve errors
    }
    mask <<= 1;
  }

  return wrCnt;
}

static size_t txtfmt_sfFlagsToStr(char * dst,
                                size_t size,
                                uint32_t flags)
{
  char * wrPtr = dst;
  size_t wrSize = 0;
  uint32_t i = 0; // bit position
  dst[0] = '\0'; // if nothing new, clear old
  while (flags)
  {
    if (flags & 1)
    {
      //dst = snprintf(dst, size - wrCnt, "%s ", enumstr_sfFlag(i));
      wrPtr = stpncpy(wrPtr, enumstr_sfFlag(i), size - wrSize);
      wrSize = dst - wrPtr;
    }
    flags >>= 1;
    i++;
  }
  ENUM_TO_STR(enum aaa, aaa)
  return wrSize;
}
