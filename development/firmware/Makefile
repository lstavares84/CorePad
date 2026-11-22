CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -Werror -pedantic -O2
.PHONY: test arm
build:
	mkdir -p build
test: build
	$(CC) $(CFLAGS) corepad.c test_corepad.c -o build/test_corepad
	./build/test_corepad
arm: build
	arm-none-eabi-gcc $(CFLAGS) -mcpu=cortex-m33 -mthumb -ffreestanding -c corepad.c -o build/corepad_m33.o
