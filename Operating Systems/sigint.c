#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
void sigint_handler(int sig){
  printf("SIGINT signal caught\n");
  exit(0);
}

int main(){
  if(signal(SIGINT, sigint_handler) == SIG_ERR)
    perror("signal error");
  pause(); //wait for the signal to be caught
  return 0;
}