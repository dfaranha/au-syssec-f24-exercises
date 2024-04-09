#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFSIZE 8

void print_flag(void);
void print_buf(int* buf, size_t len);
void calc(void);

void print_flag(void)
{
    system("cat flag.txt");
}

void print_buf(int* buf, size_t len)
{
    printf("REG:\tVAL\n");
    for (size_t i = 0; i < len; ++i)
        printf("%zu:\t0x%x\n", i, buf[i]);
}


void num_storage(void)
{
    int buf[BUFSIZE] = {0};
    char* line = NULL;
    size_t len = 0;
    ssize_t ret = 0;
    long long idx = 0;
    int val = 0;
    print_buf(buf, BUFSIZE);
    while (true)
    {
        printf("Index: ");
        ret = getline(&line, &len, stdin);
        if (ret <= 0 || strcmp(line, "\n") == 0)
            break;
        idx = strtoll(line, NULL, 10);
        if (idx >= BUFSIZE)
        {
            printf("Index too large\n");
            continue;
        }

        printf("Value: ");
        ret = getline(&line, &len, stdin);
        if (ret <= 0 || strcmp(line, "\n") == 0)
            break;
        val = atoi(line);

        buf[idx] = val;

        print_buf(buf, BUFSIZE);
    }
    free(line);
}


int main()
{
    setbuf(stdout, NULL);

    num_storage();

    return 0;
}
