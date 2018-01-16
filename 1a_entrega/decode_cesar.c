#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

char abc[] = "abcdefghijklmnopqrstuvwxyz";

void usage()
{
    char buff[80];
    sprintf(buff, "./decode (Cesar offset)\n");
    write(1, buff, strlen(buff));
    exit(EXIT_FAILURE);
}

void error(int line, char *msg)
{
    char buff[128] = {0};
    sprintf(buff, "error en linea %d: %s", line, msg);
    perror(buff);
    exit(EXIT_FAILURE);
}

int my_read(int fd, void *c, int size, int line)
{
    int ret = read(fd, c, size);
    if (ret < 0)
        error(line, "read");
    return ret;
}

int my_write(int fd, void *c, int size, int line)
{
    int ret = write(fd, c, size);
    if (ret < 0)
        error(line, "write");
    return ret;
}

int my_lseek(int fd, int offset, int whence, int line)
{
    int ret = lseek(fd, offset, whence);
    if (ret < 0)
        error(line, "lseek");
    return ret;
}

int my_open(char* fileName, int flags, int line)
{
    int fd = open(fileName, flags);
    if (fd < 0) {
        error(line, "open");
    }
    return fd;
}

int main(int argc, char *argv[])
{
    if (argc < 2) {
        usage();
    }
    int messageDescriptor = my_open("./2017_09_08_17_31_04_albert.lopez.alcacer.Cesar", O_RDONLY, __LINE__);
    int fileSize = my_lseek(messageDescriptor, 0L, SEEK_END, __LINE__);
    my_lseek(messageDescriptor, 0L, SEEK_SET, __LINE__);
    char fileBuffer[fileSize];
    my_read(messageDescriptor, fileBuffer, sizeof(fileBuffer), __LINE__);
    close(messageDescriptor);
    int i;
    for (i = 0; i < strlen(fileBuffer); i++) {
        char c = fileBuffer[i];
        int pos;
        int mayus;
        if (c >= 97 && c <= 122) {
            pos = ((c - 97) - atoi(argv[1])) % 26;
            mayus = 0;
        } else if (c >= 65 && c <= 90) {
            pos = ((c - 65) - atoi(argv[1])) % 26;
            mayus = 1;
        }
        if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
            if (pos < 0) pos += 26;
            if (mayus)
                fileBuffer[i] = abc[pos] - 32;
            else
                fileBuffer[i] = abc[pos];
        }
    }
    int ofd = open("./decoded_cesar.txt", O_CREAT | O_RDWR, S_IRWXU);
    if (ofd < 0) {
        error(__LINE__, "new file creation");
    }
    my_write(ofd, fileBuffer, strlen(fileBuffer), __LINE__);
    exit(0);
}
