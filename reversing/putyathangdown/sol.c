#include <stdio.h>

//char guess[] = "DawgCTF{.tIesreveRdnAtIpilF,nwoDgnihTyMtuP}";
char guess[] = "\x41\xf5\x51\xd1\x4d\x61\xd5\xe9\x69\x89\x19\xdd\x9\x11\x89\xcb\x9d\xc9\x69\xf1\x6d\xd1\x7d\x89\xd9\xb5\x59\x91\x59\xb1\x31\x59\x6d\xd1\x8b\x21\x9d\xd5\x3d\x19\x11\x79\xdd";

void reverse_it(){
        unsigned int  bits = sizeof(char) * 8;
        char reverse_char = 0;
        char c;
        char temp;

        for(int k = 0; k < 43; k++){
                c = guess[k];
                for (int i = 0; i < bits; i++){
                        temp = (c & (1 << i));
                        if(temp){
                                reverse_char |= (1 << ((bits - 1) - i));
                        }
                }
                guess[k] = reverse_char;
		reverse_char = 0;
        }

        for(int i = 0; i < 43 / 2; i++){
                temp = guess[i];
                guess[i] = guess[43 - i - 1];
                guess[43 - i - 1] = temp;
        }

}

void flip_it(){
        for(int i = 0; i < 43; i++){
                guess[i] = guess[i] ^ 0xff;
        }
}

void print_hex(const char *s)
{
  while(*s)
    printf("\\x%x", *s++ & 0xff);
  printf("\n");
}

int main(){
	flip_it();
	print_hex(guess);
	reverse_it();
	print_hex(guess);
	printf("%s", guess);
}
