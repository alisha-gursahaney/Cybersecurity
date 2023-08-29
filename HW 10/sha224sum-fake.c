#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc > 1 && strcmp(argv[1], "--be-evil") == 0) {
        printf("Some evil text. I will hack you!\n");
        printf("This is the evil code with multiple lines!\n");
    } else {
        printf("This is my evil one line code!\n");
    }

    execl("/usr/bin/sha224sum.original", "sha224sum.original", argv[1], NULL);
    perror("execl failed");
    exit(EXIT_FAILURE);
}
