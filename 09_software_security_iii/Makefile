CC = gcc
CFLAGS = -g -O3 -w
# CFLAGS = -g -O3 -Wall -Wextra

.phony: all clean

all: address address_asan thread thread_tsan undefined undefined_ubsan

%: %.c
	$(CC) -o $@ $(CFLAGS) $^

address_asan: address.c
	$(CC) -fsanitize=address -o $@ $(CFLAGS) $^

thread: thread.c
	$(CC) -pthread -o $@ $(CFLAGS) $^

thread_tsan: thread.c
	$(CC) -fsanitize=thread -pthread -o $@ $(CFLAGS) $^

undefined_ubsan: undefined.c
	$(CC) -fsanitize=undefined -o $@ $(CFLAGS) $^


clean:
	rm -f address address_asan thread thread_tsan undefined undefined_ubsan
