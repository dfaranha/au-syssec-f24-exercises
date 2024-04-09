.phony: clean

random_password: random_password.c
	gcc -Wall -Wextra -m32 -no-pie -Wl,-z,norelro -o random_password random_password.c

clean:
	rm -f random_password
