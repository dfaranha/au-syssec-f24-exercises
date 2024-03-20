#include <stdio.h>
#include <stdint.h>
#include <unistd.h>


void win() {
    printf("Success!\n");
}

void vuln() {
    char name[32];

    printf("win is located at %p\n", win);
    printf("Please enter your name: ");
    read(0, name, 320);
    printf("Hello %s!\n", name);
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
}
