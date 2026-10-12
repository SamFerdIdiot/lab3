#include <stdio.h>
#include <stdlib.h> 
#include <string.h> //strlen(msg) для write
#include <unistd.h>
#include <sys/wait.h> 
#include <time.h> //time, localtime, strftime

int main(void)
{
int fd[2]; // масив из 2 чисел для 0 чтение 1 запись 
if (pipe(fd) == -1) // просит у ядра создать канал успех 0 ошибка -1 
    {
perror("pipe"); // печатает ошибку 
return 1;
    }

pid_t pid = fork(); // колнирует процесс также fd отличие pid 
// потомок 0
// родитель pid потомка
// ошибка -1 
if (pid == -1) 
    {
perror("fork");
return 1;
    }

if (pid == 0) 
    {
// потомок читает закрываем запись
close(fd[1]);

sleep(5);

char buf[256];
ssize_t n = read(fd[0], buf, sizeof(buf) - 1); //тчитаем строку от родителя
if (n > 0)
        {
buf[n] = '\0'; // read не добавляет \0, ставим сами

time_t now = time(NULL); //текущее время потомка в секундах
char tbuf[64];
strftime(tbuf, sizeof(tbuf), "%H:%M:%S", localtime(&now));

printf("потомок: время %s, получено: %s\n", tbuf, buf);
        }
fflush(stdout); // кидываем буфер 
close(fd[0]);
_exit(0); // убиваем потомка
    }

close(fd[0]); // закрываем чтение, пишем

time_t now = time(NULL); // время родителя
char tbuf[64];
strftime(tbuf, sizeof(tbuf), "%H:%M:%S", localtime(&now));

char msg[256];
snprintf(msg, sizeof(msg), "время родителя %s, pid родителя %d",
         tbuf, (int)getpid()); // формируем строку время pid

write(fd[1], msg, strlen(msg)); // дескриптор, откуда, сколько байт 
close(fd[1]); // закрываем запись
wait(NULL); // дождаться потомка
return 0;
}