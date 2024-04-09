#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

const char* shell = "false && /bin/sh";


void hello(void)
{
    char name[32];
    printf("What's your name?\n");
    fgets(name, 32, stdin);
    if (strchr(name, '%') && strchr(name, 'n'))
        exit(1);
    printf("Hello ");
    printf(name);
}

void login(void)
{
    char rand[16];
    char input[16];

    printf("Please enter the password\n");
    fgets(input, 64, stdin);

    int fd = open("/dev/urandom", O_RDONLY);
    if (fd == -1)
    {
        exit(1);
    }
    read(fd, rand, 16);
    close(fd);

    if (memcmp(input, rand, 16) == 0)
    {
        printf("Shell for you :)\n");
        system(shell);
    }
    else
    {
        printf("Sorry, wrong password!\n");
    }
}


int main()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    hello();
    login();
    return 0;
}
