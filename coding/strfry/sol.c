#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char** argv){
  	static struct random_data rdata;
	static char state[32];
	rdata.state = NULL;
 	initstate_r (atoi(argv[1]) ^ atoi(argv[2]),
                    	state, sizeof (state), &rdata);
	while(1){
		char string[50];
		scanf("%s", string);
  		size_t len = strlen (string);
  		if (len > 0){
    			for (size_t i = 0; i < len - 1; ++i){
        			int32_t j;
        			random_r (&rdata, &j);
        			j = j % (len - i) + i;
        			char c = string[i];
        			string[i] = string[j];
        			string[j] = c;
      			}
		}
  		printf("%s\n", string);
	}
	return 0;
}
