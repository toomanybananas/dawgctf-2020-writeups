#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "unistd.h"

void win(){
	printf("I'm not sure how, but your terrible leadership worked!");
        char *argv[] = {"/bin/cat", "flag.txt", 0};
        execve("/bin/cat", argv, 0);
}

void lose1(){
	printf("\nYour test comes back negative, but no one trusts your doctor.\n");
	printf("The country goes into mass hysteria and society collapses.\n");
}

void lose2(){
	printf("\nThe Christian community praises your good sense while buying up all the toilet paper in the country.\n");
	printf("As the shelves run dry and society collapses.\n");
}

void lose3(){
	printf("\nHospitals become overrun with cases and many people without healthcare can't afford treatment\n");
	printf("Society collapses as hospitals fill.\n");
}
void lose4(){
	printf("\nNo one under the age of 50 cares about the emergency and bars have their best weekend in months.\n");
	printf("The virus rapidly spreads and society collapses.\n");
}

void no_panic(){
	char answer[64];
	printf("\nExcellent choice. It's all a hoax anyway!\n");
	printf("Oof WHO just announced it's a pandemic AND American treasure Thomas Hanks is quarentined...\n");
	printf("1. Get tested and show everyone your immune system is the best. Just the greatest\n");
	printf("2. Call for a national day of prayer. God will save us!\n");
	fgets(answer, 50, stdin);
	printf("You chose: ");
	printf(answer);
	if(strncmp("1", answer, 1) == 0){
		lose1();
	}else if(strncmp("2", answer, 1) == 0){
		lose2();
	}
}

void close_borders(){
	char answer[64];
	printf("\nSo we closed our borders. Weren't we doing that anyway with the wall?\n");
	printf("It's still spreading within our borders what do we do now?\n");
	printf("1. Reassure everyone the country can handle this. Our healthcare system is the best. Just the greatest.\n");
	printf("2. Make it a national emergency. Show the people we don't need Bernie's healthcare plan.\n");
	fgets(answer, 50, stdin);
	printf("You chose: ");
	printf(answer);
	if(strncmp("1", answer, 1) == 0){
		lose3();
	}else if(strncmp("2", answer, 1) == 0){
		lose4();
	}
}

void play_game(){
	char answer[64];
	printf("Welcome to this choose your own adventure game!\n");
	printf("You're President Ronald Drump and are tasked with leading the nation through this crisis.\n");
	printf("So what do you want to do?\n");
	printf("1. Close the borders.\n");
	printf("2. Tell everyone not to panic. It's just the Fake News media freaking out.\n");
	fgets(answer, 50, stdin);
	printf("You chose: ");
	printf(answer);
	if(strncmp("1", answer, 1) == 0){
		close_borders();
	}else if(strncmp("2", answer, 1) == 0){
		no_panic();
	}
}

int main(){
	play_game();
}
