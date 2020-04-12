#include <stdio.h>

void math(char loc){
	char sol = solution;
	if(sol == ((char)loc operation (char)constant)){
		puts("Correct");
	}else{
		puts("Incorrect");
	}
}

int main(){
	char loc;
	printf("Where's the elf hiding?");
	loc = fgetc(stdin);
	math(loc);
	return 0;
}
