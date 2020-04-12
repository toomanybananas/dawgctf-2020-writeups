#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

int len = 0;
char *shellcode;


void welcome(){
	printf("What's up guys welcome to my channel today we're gonna hack fornite XD\n");
	printf("So where we roppin boys?\n");
	shellcode = mmap(0, 28, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
        if (shellcode == MAP_FAILED) {
        	perror("mmap() failed");
		exit(1);
	}
}

int loot_lake(){
	if(len < 24){
		*(shellcode + (len++)) = '\xc0';
		*(shellcode + (len++)) = '\x40';
		*(shellcode + (len++)) = '\xcd';
		*(shellcode + (len++)) = '\x80';
		return 0;
	}
	return 1;
}

int lonely_lodge(){
	if(len < 24){
		*(shellcode + (len++)) = '\xc1';
		*(shellcode + (len++)) = '\x89';
		*(shellcode + (len++)) = '\xc2';
		*(shellcode + (len++)) = '\xb0';
		return 0;
	}
	return 1;
}

int tilted_towers(){
	if(len < 24){
		*(shellcode + (len++)) = '\x31';
		*(shellcode + (len++)) = '\xc0';
		*(shellcode + (len++)) = '\x50';
		*(shellcode + (len++)) = '\x68';
		return 0;
	}
	return 1;
}

int snobby_shores(){
	if(len < 24){
		*(shellcode + (len++)) = '\x68';
		*(shellcode + (len++)) = '\x2f';
		*(shellcode + (len++)) = '\x62';
		*(shellcode + (len++)) = '\x69';
		return 0;
	}
	return 1;
}

int dusty_depot(){
	if(len < 24){
		*(shellcode + (len++)) = '\x0b';
		*(shellcode + (len++)) = '\xcd';
		*(shellcode + (len++)) = '\x80';
		*(shellcode + (len++)) = '\x31';
		return 0;
	}
	return 1;
}

int junk_junction(){
	if(len < 24){
		*(shellcode + (len++)) = '\x2f';
		*(shellcode + (len++)) = '\x2f';
		*(shellcode + (len++)) = '\x73';
		*(shellcode + (len++)) = '\x68';
		return 0;
	}
	return 1;
}

int greasy_grove(){
	if(len < 24){
		*(shellcode + (len++)) = '\x6e';
		*(shellcode + (len++)) = '\x89';
		*(shellcode + (len++)) = '\xe3';
		*(shellcode + (len++)) = '\x89';
		return 0;
	}
	return 1;
}

int win(){
	if(mprotect(shellcode, 28, PROT_EXEC) < 0){
		exit(1);
	}
	(*(void(*)()) shellcode)();
	return 0;
}

int tryme(){
	char sum[4];
	fgets(sum, 25, stdin);
	fflush(stdin);
	return 0;
}

int main(){
	welcome();
	tryme();
	return 0;
}
