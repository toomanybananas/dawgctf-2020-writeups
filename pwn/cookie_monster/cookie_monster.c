#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "unistd.h"

int saved_cookie;

void flag(){
        char *argv[] = {"/bin/cat", "flag.txt", 0};
        execve("/bin/cat", argv, 0);
}

void check_cookie(int cookie){
	if(cookie != saved_cookie){
		printf("*** Stack Smashing Detected *** : Cookie Value Corrupt!\n");
		exit(-1);
	}
}

void conversation(){
	srand(time(0));
	int cookie = rand();
	saved_cookie = cookie;
	char name[8];
	char answer[5];
	printf("\nOh hello there, what's your name?\n");
	fgets(name, 8, stdin);
	printf("Hello, ");
	printf(name);
	printf("\nWould you like a cookie?\n");
	gets(answer);
	check_cookie(cookie);
}

void print_cookie(){
	printf("               _  _\n");
	printf("             _/0\\/ \\_\n");
	printf("    .-.   .-` \\_/\\0/ \'-.\n");
	printf("   /:::\\ / ,_________,  \\\n");
	printf("  /\\:::/ \\  \'. (:::/  `\'-;\n");
	printf("  \\ `-\'`\\ \'._ `\"\'\"\'\\__    \\\n");
	printf("   `\'-.  \\   `)-=-=(  `,   |\n");
	printf("       \\  `-\"`      `\"-`   /\n");
	printf("C is for cookie is for me");
}

int main(){
	print_cookie();
	conversation();
	return 0;
}
