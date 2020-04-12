// Anna Staats
// December 17, 2019
// DawgCTF BAYUHBEE

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <poll.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

int timeout(int sol_min, int sol_sec){
    	struct pollfd mypoll = { STDIN_FILENO, POLLIN|POLLPRI };
	char k[11];
	int try_min, try_sec;
    	if(poll(&mypoll, 1, 3000)){
		scanf("%10s", k);
		try_min = atoi(strtok(k, ":"));
		if(try_min){
			try_sec = atoi(strtok(NULL, ":"));
		}else{
			return 0;
		}
		if(try_min == sol_min && try_sec == sol_sec){
			return 1;
		}else{
			return 0;
		}
	}
	return 0;
}

void print_flag(){
	printf("Dang you're pretty quick\nflag: DawgCTF{doe5n't_ruNN1ng_sUcK?!}\n");
}

int main(){
	printf("-----------------------------------------\nHi, I'm Anna and I really like running\nI'm too broke to get a gps watch though :(\nThink you can figure out my average pace?\n-----------------------------------------\n");
	FILE* stream = fopen("strava.csv", "r");
	char line[1024];
	int i = 0;
	int correct = 1;
	while (fgets(line, 1024, stream) && correct){
		char* dist = strtok(line, ",");
		char* time = strtok(NULL, ",");
       		printf("I ran %s in %s What's my pace? \n", dist, time);
		int hour = atoi(strtok(time, ":"));
		int min = atoi(strtok(NULL, ":"));
		int sec = atoi(strtok(NULL, ":"));
		double total = (hour*60*60) + (min*60) + sec;
		double pace = total/atof(dist);
		int sol_min = pace / 60;
		int sol_sec = (int)pace % 60;
        	correct = timeout(sol_min, sol_sec);
		i++;
        }
	if(correct){
		print_flag();
	}else{
		printf("Ha too slow!\n");
	}
	return 0;
}
