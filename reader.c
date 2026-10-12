#include <stdio.h>
#include <time.h>
#include <fcntl.h> // open и флаги 
#include <unistd.h>

int main(void)
{
    int fd = open("myfifo", O_RDONLY); // ждёт, пока writer откроет fifo
    if (fd == -1)
    {
        perror("open"); 
        return 1;
    }

    sleep(10); 

    char buf[128];
    ssize_t n = read(fd, buf, sizeof(buf) - 1); //записываем сколько байт прочитали 
    if (n > 0)
    {
        buf[n] = '\0';
        time_t now = time(NULL);
        printf("получатель: %sполучено: %s", ctime(&now), buf);
    }
    close(fd);
    return 0;
}