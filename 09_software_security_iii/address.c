#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


char* hello(char* greeting) {
    char name[33];
    printf("What's your name?\n");
    fgets(name, 33, stdin);
    for (size_t i = 0; i < 33; ++i) {
        if (name[i] == '\n') {
            name[i] = '\0';
        }
    }

    size_t l1 = strlen(greeting);
    size_t l2 = strlen(name);
    char* buf = malloc(l1);
    assert(buf != NULL);
    strcpy(buf, greeting);
    buf[l1] = ' ';
    strncat(buf + l1 + 1, name, 32);
    return buf;
}

int* like_pointers() {
    int answer = 0;
    int* p = &answer;
    char buf[16];
    fgets(buf, 16, stdin);
    if (strncmp(buf, "YES", 3) == 0) {
        *p = 42;
    }
    return p;
}


void stuff(char** argv) {
    size_t l1 = strlen(argv[1]);
    size_t l2 = strlen(argv[2]);

    char* s1 = malloc(l1);
    /* s1[l1] = '\0'; */
    printf("s1 @ %p\n", s1);
    strncpy(s1, argv[1], l1);
    printf("s1 = %s\n", s1);

    free(s1);

    char* s2 = malloc(l2 + 1);
    strncpy(s2, argv[2], l2);
    s2[l2] = '\0';
    printf("s2 @ %p\n", s2);
    printf("s2 = %s\n", s2);

    printf("s1 = %s\n", s1);
    printf("s2 = %s\n", s2);
    free(s1);
    free(s2);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <input> <input>\n", argv[0]);
        return 1;
    }

    char* greeting = hello("Moin");
    printf("============== %s ==============\n", greeting);

    puts("Do you like pointers?");
    int* answer = like_pointers();
    /* printf("answer %d @ %p\n", *answer, answer); */
    if (*answer == 42) {
        puts("great!");
    } else {
        puts("WTF???");
    }
    free(answer);

    stuff(argv);

    return 0;
}
