#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // print the currend real and effective user ids
    uid_t uid = getuid();
    uid_t euid = geteuid();
    printf("Real user id: %d\n", uid);
    printf("Effective user id: %d\n", euid);
}
