#include <stdio.h>
#include <unistd.h>
#include <stdlib.h> 
#include <fcntl.h>

int main(int argc, char *argv[])
{
    int fd;
    char *buf;
    int len= atoi(argv[1]);
    
    char path[] = "integer_of.txt";

    fd = open(path, O_RDONLY);

    if (len > 8000) {return 0; }
    buf = malloc(len);
    read(fd, buf, len); /* len casted to unsigned and overflows */
    return 0;
}