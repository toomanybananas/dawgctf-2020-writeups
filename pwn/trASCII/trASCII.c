// gcc -m32 -fstack-protector --param=ssp-buffer-size=72 -no-pie -z execstack -Wl,-Ttext=0x52314d00 trASCII.c -o trASCII
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char trash[10000];

void compact(){
	char compact[64] = {0};
	int i = 0;
	int len = 0;
	printf("What garbage do you have for us today?\n");
	fgets(trash, 10000, stdin);
	len = strlen(trash);
	if(len == 0){
		printf("You didn't enter any trash :(\n");
		exit(-1);
	}
	trash[len-1] = '\x00';
	for(i = 0; i < len - 1; i++){
		int count = 1;
		while(i < len - 1 && trash[i] == trash[i + 1]){
			count++;
			i++;
		}
		if(trash[i] > 0x7a || trash[i] < 0x30){
			printf("That\'s not trash, that\'s recycling\n");
			exit(-1);
		}
		compact[strlen(compact) + 1] = '\x00';
		compact[strlen(compact)] = trash[i];
		sprintf(&compact[strlen(compact)], "%d", count);
	}
	memset(trash, 0, sizeof(trash));
	strcpy(trash, compact);
	printf("Thanks for the trash! Here's how I compressed it: %s\n", trash);
}

int main(){
	setvbuf(stdout, 0, 2, 0);
	setvbuf(stdin, 0, 2, 0);
	printf("Welcome to trASCII, a program by trashcanna!\n");
	printf("We'll take all your random ASCII garbage and convert it into something magical!\n");
	compact();
	return 0;
}
