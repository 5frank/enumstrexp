echo " ----------- GCC: ------------ "
PROG_NAME=test_utils
gcc -o $PROG_NAME.o $PROG_NAME.c -lm -O0
#-Wall -Wswitch-enum -Wswitch-default

#-Wtraditional-conversion
#-Wconversion


echo " ----------- Exe: ------------ "
./$PROG_NAME.o
#rm $PROG_NAME.o
