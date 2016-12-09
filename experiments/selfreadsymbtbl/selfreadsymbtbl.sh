echo " ----------- GCC: ------------ "
PROG_NAME=selfreadsymbtbl


#PROG_PP_FILE="${PROG_NAME}_pp.c"
#gcc -E $PROG_NAME.c -o $PROG_PP_FILE
gcc -o $PROG_NAME.o $PROG_NAME.c -lm -O0 -g -ggdb -Wall -Wextra \
-ldl -Wl,--export-dynamic -fvisibility=hidden -rdynamic

#nm -C  $PROG_NAME.o | grep ___mkenumstr_cfg

#-Wtraditional-conversion
#-Wconversion

#sh run.sh
echo " ----------- Exe: ------------ "
./$PROG_NAME.o
#rm $PROG_NAME.o
