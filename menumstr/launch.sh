#!/bin/sh
# this script is needed as python has to be invoked by GDB
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in
SCRIPTPATH=$(dirname "$SCRIPT")
SHELL_ARGS="$@"; #$(echo $@ | tr -d ' ')



echo " ----------- GCC: ------------ "
PROG_NAME=main
gcc -o $PROG_NAME.o $PROG_NAME.c -lm -ldl -O0 -g3 -ggdb -std=gnu99 -Wall \
-export-dynamic -fvisibility=hidden -fno-eliminate-unused-debug-types \
-I "$SCRIPTPATH" \
-I "$SCRIPTPATH/../test/" \
-I "$SCRIPTPATH/../test/codegen" 
#-Wtraditional-conversion
#-Wconversion
#nm |
#SYMADDRS=$(nm -C main.o | grep job | cut -d ' ' -f 1)
#echo $SYMADDRS

#echo " ----------- Exe: ------------ "
#./$PROG_NAME.o $SYMADDRS
#rm $PROG_NAME.o


SYMB_OBJ="$SCRIPTPATH/$PROG_NAME.o"

# gdb: .gdbinit initialization file is executed unless options -nx, -n or -nh.

#export SRC_DIR=$(cd ..; pwd)
#echo $SCRIPTPATH

gdb -n -silent -batch \
    -eval-command="set \$SYMB_OBJ=\"$SYMB_OBJ\"" \
    -eval-command="set \$SHELL_ARGS=\"$SHELL_ARGS\"" \
    -eval-command="source $SCRIPTPATH/enumstrexp.py"

#  -eval-command="quit"
