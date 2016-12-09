
PROG_NAME=test_ccoptimizer

#CC = arm-none-eabi-gcc
#CC = gcc

arm-none-eabi-gcc -g -O0 -c -fverbose-asm -Wa,-adhln  $PROG_NAME.c \
-O3 -lm  -g -std=gnu99 \
> $PROG_NAME.s
