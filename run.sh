#!/bin/sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in
SCRIPTPATH=$(dirname "$SCRIPT")
ELF_PATH="$SCRIPTPATH/../elof_ma_fw/build/ma2img.elf"

#strip spaces
RTDVARSARG=$(echo $@ | tr -d ' ')
echo $RTDVARSARG
gdb -silent -batch $ELF_PATH\
      -eval-command="source enumstrexp.py" \
      -eval-command="rtd-export $RTDVARSARG" \
      -eval-command="quit"

