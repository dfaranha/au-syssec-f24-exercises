#include <stdio.h>
#include <stdint.h>
#include <unistd.h>


void vuln() {
    char name[32];

    printf("name is located at %p\n", name);
    printf("Please enter your name: ");
    read(0, name, 320);
    printf("Hello %s!\n", name);
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    vuln();
}
