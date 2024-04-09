#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


#define N 100

typedef struct {
    uint8_t padding;
    uint32_t data[N];
} __attribute__ ((packed))
data_t;

void add_numbers(int x, int y) {
    printf("%d\n", x);
    printf("%d\n", y);

    // can you fool this check for overflows/wrap arounds?
    if (y >= 0 && x + y < x) {
        printf("warning: overflow!\n");
    } else if (y < 0 && x + y > x) {
        printf("warning: overflow!\n");
    } else {
        printf("no overflow happened :)\n");
    }
    printf("%d\n", x + y);
}


uint32_t sum(uint32_t* p, size_t n) {
    printf("p = %p\n", p);
    uint32_t s = 0;
    for (size_t i = 0; i < n; ++i) {
        s += p[i];
    }
    return s;
}

void square(uint32_t* p, size_t n) {
    uint32_t* data = p;
    // replace the previous line with the following and see what happens
    // uint32_t* data = __builtin_assume_aligned(p, 16);
    for (size_t i = 0; i < n; ++i) {
        data[i] = data[i] * data[i];
    }
    puts("success");
}

void stuff() {
    data_t d;
    for (size_t i = 0; i < N; ++i) {
        d.data[i] = i;
    }
    square(d.data, N);
    uint32_t s = sum(d.data, N);
    printf("s = %ld\n", (long)s);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s <number> <number>\n", argv[0]);
        return 1;
    }

    int x = atoi(argv[1]);
    int y = atoi(argv[2]);
    add_numbers(x, y);

    stuff();

    return 0;
}
