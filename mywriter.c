#include <stdio.h>
#include <string.h>
#include <time.h>
#include <fcntl.h>
#include <unistd.h>

int main(void)
{
    int fd = open("myfifo", O_WRONLY); // ждёт, пока reader откроет fifo
    if (fd == -1)
    {
        perror("open");
        return 1;
    }

    time_t now = time(NULL);
    char msg[128];
    snprintf(msg, sizeof(msg), "pid %d, время %s", (int)getpid(), ctime(&now));

    write(fd, msg, strlen(msg));
    close(fd);
    return 0;
}