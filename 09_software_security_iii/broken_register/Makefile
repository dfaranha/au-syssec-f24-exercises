CC=gcc
CFLAGS=-Wall -Wextra -std=gnu11 -m32 -no-pie -fstack-protector

.phony: clean

broken_register: broken_register.c
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -rf broken_register
