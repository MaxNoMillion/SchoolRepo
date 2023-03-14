#include <signal.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(){
    pid_t pid = fork();
    if(pid == 0){
      pause(); //wait for signal to arrive 
      printf("This line should be unreachable");
      exit(0);
    }else{
      printf("killing the child process\n");
      //kill(pid, SIGKILL);
      kill(pid, SIGCONT);
      wait(NULL);
      exit(0);
    }

}