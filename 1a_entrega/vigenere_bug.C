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
    sprintf(buff, "./decode\n");
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

int my_round(float f) {
    int i = (int)f;
    int r_i;
    if (f != i) 
        r_i = i + 1;
    else 
        r_i = i;
    return r_i;
}

int* getFreqs(char* buffer)
{
    static int letterFreq[26] = {0};
    int bufferSize = strlen(buffer);
    int j;
    for (j = 0; j < bufferSize; j++)
    {
        char c = buffer[j];
        int pos;
        if (c >= 97 && c <= 122)
        {
            pos = (c - 97) % 26;
        }
        else if (c >= 65 && c <= 90)
        {
            pos = (c - 65) % 26;
        }
        if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90))
        {
            if (pos < 0)
                pos += 26;
            letterFreq[pos]++;
        }
    }
        //printf("freq: %d\n", letterFreq[j]);
    return letterFreq;
}

char mostFreq(char* cesarG) {
    int j, posMost, sizeMost;
    int *freqs = getFreqs(cesarG);
    sizeMost = 1;
    for (j = 0; j < 26; j++) { 
        if (freqs[j] >= sizeMost) {
            sizeMost = freqs[j];
            posMost = j;
        }
    }
    
    return abc[posMost];
}


int main(int argc, char *argv[])
{
    int messageDescriptor = my_open("./2017_09_08_17_31_04_albert.lopez.alcacer.Vigenere", O_RDONLY, __LINE__);
    int fileSize = my_lseek(messageDescriptor, 0L, SEEK_END, __LINE__);
    my_lseek(messageDescriptor, 0L, SEEK_SET, __LINE__);
    char fileBuffer[fileSize];
    char preProcessed[fileSize];
    my_read(messageDescriptor, fileBuffer, sizeof(fileBuffer), __LINE__);
    close(messageDescriptor);

    int i, j;
    j = 0;
    for (i = 0; i < fileSize; i++) {
        char c = fileBuffer[i];
        if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
            preProcessed[j++] = c;
        }
    }
    preProcessed[j] = '\0';

    //my_write(1, preProcessed, strlen(preProcessed), __LINE__);

    //No da el tamaño correcto, se ha hardcodeado el tamaño de la clave!
    int *letterFreq = getFreqs(preProcessed);
    int preFileSize = strlen(preProcessed);
    float k0, k0n = 0;
    for (i = 0; i < 26; i++) {
        k0n += letterFreq[i] * (letterFreq[i] - 1);
    }
    k0 = (k0n/(preFileSize * (preFileSize - 1)));
    
    float keyLengthf = (0.067 - 1/26)/(k0 - 1/26);
    int keyLength = my_round(keyLengthf);

    printf("Obtained keyLength is: %d\n", keyLength);
    keyLength = 4;
    printf("KeyLength in fact is: %d\n", keyLength);

    //Now start to do cesar in the different groups of keysize
    
    int c = my_round((float)preFileSize/(float)keyLength);
    char cesarGroups[keyLength][c + 1];
    for (i = 0; i < keyLength; i++)
        cesarGroups[i][0] = '\0';
    for (i = 0; i < preFileSize; i++)
        strncat(&cesarGroups[i % keyLength][0], &preProcessed[i], 1);

    char mostFreqL[keyLength];
    int *keyValue = calloc(keyLength, sizeof(int));
    for (i = 0; i < keyLength; i++) {
        mostFreqL[i] = mostFreq(&cesarGroups[i][0]);
        printf("Most freq letter #%d -> %c\n", i, mostFreqL[i]);
        keyValue[i] = mostFreqL[i] - 'e';
    }
    printf("Key is: ");
    for (i = 0; i < keyLength; i++) {
        int pos;
        if (keyValue[i] < 0)
            pos = keyValue[i] + 26;
        else
            pos = keyValue[i] % 26;
        printf("%c", abc[pos]);
    }
    printf("\n");

    //key: SNOW
    int keyNum = -1;
    for (i = 0; i < fileSize; i++) {
        char c = fileBuffer[i];
        int pos;
        int keyNumPos;
        if (c >= 97 && c <= 122)
            pos = c - 97;
        else if (c >= 65 && c <= 90) 
            pos = c - 65; 
        if ((c >= 97 && c <= 122) || (c >= 65 && c <= 90)) {
            keyNumPos = (++keyNum) % keyLength;
            pos = (pos - keyValue[keyNumPos]) % 26;
            if (pos < 0) pos += 26;
            fileBuffer[i] = abc[pos];
        }
    }

    int ofd = open("./decoded_vigenere.txt", O_CREAT | O_RDWR, S_IRWXU);
    if (ofd < 0) {
        error(__LINE__, "new file creation");
    }
    my_write(ofd, fileBuffer, fileSize, __LINE__);
    exit(0);
    
}