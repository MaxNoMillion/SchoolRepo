#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <limits.h>

void sigint_handler(int sig){
  return;
}

void snooze(int time){
  int stime = sleep(time);
  printf("Slept %d secs. out of %d!\n", time - stime, time);
}

int main(int argc, char *argv[]){
  if(signal(SIGINT, sigint_handler) == SIG_ERR)
    perror("signal error");
 snooze(atoi(argv[1]));
  exit(0);
}