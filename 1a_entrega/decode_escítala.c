#include <sys/types.h>
#include <sys/stat.h>
#include <stdlib.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

void usage()
{
    char buff[80];
    sprintf(buff, "./decode_escítala (number of columns provisional Key)\n");
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

int my_open(char *fileName, int flags, int line)
{
    int fd = open(fileName, flags);
    if (fd < 0)
    {
        error(line, "open");
    }
    return fd;
}




int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        usage();
    }

    int messageDescriptor = my_open("./2017_09_08_17_31_04_albert.lopez.alcacer.Escitalo", O_RDONLY, __LINE__);
    int fileSize = my_lseek(messageDescriptor, 0L, SEEK_END, __LINE__);
    my_lseek(messageDescriptor, 0L, SEEK_SET, __LINE__);

    int filas, columnas;
    columnas = atoi(argv[1]);

    float r = (fileSize / (float)columnas);
    int rent = (int)r;
    if (r != rent) 
        filas = rent + 1;
     else 
        filas = rent;

    char kmat[filas][columnas];
    printf("Filas %d, Columnas %d\n", filas, columnas);
    int i;
    char c;
    for (i = 0; i < filas; i++) 
        my_read(messageDescriptor, &kmat[i][0], columnas, __LINE__);    

    char decodedMat[columnas][filas];
    int j;
    for (i = 0; i < columnas; i++)
        for (j = 0; j < filas; j++)
            decodedMat[i][j] = kmat[j][i];

    int ofd = open("./decoded_escitalo.txt", O_CREAT | O_RDWR, S_IRWXU);
    if (ofd < 0)
        error(__LINE__, "new file creation");
    my_write(ofd, decodedMat, fileSize, __LINE__);
}
