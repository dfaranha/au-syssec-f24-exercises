#include <stdio.h>
#include <stdint.h>
#include <unistd.h>


void win() {
    printf("Success!\n");
}

void vuln() {
    uint64_t x = 0x42;
    char name[32];

    printf("Please enter your name: ");
    read(0, name, 320);
    printf("Hello %s!\n", name);

    printf("x == %lx\n", x);
    if (x == 0x1337) {
        win();
    }
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
}
