CC = gcc
CFLAGS = -Wall -Wextra -O0  -fno-stack-protector -no-pie

.phony: all clean

all: print_user_id toctou flag.txt overflow1 overflow2 overflow3

print_user_id: print_user_id.c
	$(CC) -o $@ $(CFLAGS) $^

toctou: toctou.c
	$(CC) -o $@ $(CFLAGS) $^
	sudo chown root $@
	sudo chmod u+s $@

flag.txt:
	echo "flag{success!}" > $@
	sudo chown root:root $@
	sudo chmod go-rwx $@

overflow1: overflow1.c
	$(CC) -o $@ $(CFLAGS) $^

overflow2: overflow2.c
	$(CC) -o $@ $(CFLAGS) $^

overflow3: overflow3.c
	$(CC) -o $@ $(CFLAGS) -z execstack $^


clean:
	rm -f toctou
	rm -f flag.txt
	rm -f overflow1 overflow2 overflow3 print_user_id
