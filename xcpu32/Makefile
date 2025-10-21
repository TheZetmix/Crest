C = gcc
CFLAGS = -I./emu -I./src/cpu -g
LDFLAGS = -lX11

build: src/cpu/cpu.c emu/libterm.c
	$(CC) $(CFLAGS) -o ./build/cpu $^ $(LDFLAGS)

