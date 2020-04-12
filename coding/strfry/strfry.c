#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <poll.h>
#include <time.h>
#include <unistd.h>

int timeout(char* fried){
        struct pollfd mypoll = { STDIN_FILENO, POLLIN|POLLPRI };
        char user_input[50];
        if(poll(&mypoll, 1, 3000)){
		fgets(user_input, 50, stdin);
		if(memcmp(fried, user_input, strlen(fried))){
			return 0;
		}
		return 1;
        }
        return 0;
}

int play_game(){
	char user_input[50] = "\0";
	char strings[][50] = {"DogeCTF{D@nc3_w1th_mY_d0gs_1n_tH3_n1ghTt1m3}",
		  "DogeCTF{T@k3_1t_wH1p_1t_1nT3rm1$$10n}",
		  "DogeCTF{l3t_th3_b1rd$_fLy}",
		  "DogeCTF{th3y_tH1nK_w3_UsEd_@_ch34t_C0d3}",
		  "DogeCTF{WhY_y0u_k33p_l00k1n_@t_m3}",
		  "DogeCTF{R41nDr0p$_Dr0p_top$}",
		  "DogeCTF{b@D_anD_b0uj33}",
		  "DogeCTF{Im_r1D1n_4r0und_in_@_c0up3}",
		  "DogeCTF{B1tch_1m_4_D0g_woof}",
		  "DogeCTF{W3_D1D_th3_m0$t_Y3@h}",
		  "DogeCTF{D4bb1n_0n_3m_lik3_the_usu@l}",
		  "DogeCTF{1m_Y0ung_4nD_rich}",
		  "DogeCTF{1n_th3_cr0ckpot}",
		  "DogeCTF{0ut3r_$pace_KiD_CuD1}",
		  "DogeCTF{$4v@g3_ruthl3$s}",
		  "DogeCTF{4nD_Y0u_kn0w_w3_winn1n}",
		  "DogeCTF{W3_c4m3_fr0m_n0th1n_to_$0methin}",
		  "DogeCTF{$3v3nt33n_f1v3_s@me_c0l0r_T-$hirt}",
		  "DogeCTF{M@m4_t0lD_m3}",
		  "DogeCTF{real_fr0g_3ye$}",
		  "DogeCTF{D1vin_0ff_th3_$t4g3}",
		  "DogeCTF{T@k3_mY_sh0e$_4nd_w@lk_4_m1l3}",
		  "DogeCTF{W@lk_1t_lik3_1_t4lk_it}",
		  "DogeCTF{$@y_th4t_w3_b33n_be3f1ng_D0g}",
		  "DogeCTF{Y0_Y3@h_d@t_w@y}",
		  "DogeCTF{put_th4t_th1nG_in_sp0rt}",
		  "DogeCTF{T4k3_th3_@1r_0ut_th3_b4ll}",
		  "DogeCTF{Th3_c0upe_c@m3_1mp0rteD}",
		  "DogeCTF{It_g0t_fl4me$_oUt_th3_r34r$}",
		  "DogeCTF{Wh3n_1_coulD_ju$t_h0p_1n_@_P0r$ch3}"
	};
	for(int i = 0; i < 30; i++){
		printf("Unscrambled String: %s\n", strings[i]);
		if(!timeout(strfry(strings[i]))){
			return 0;
		}
	}
	return 1;
}

void print_flag(){
	printf("Nice job! Here's your flag: DawgCTF{3th0s_p@th0s_l0g0s_m1g0s}\n");
}

void print_loss(){
	printf("Wrong! You need to control the bag now.\n");
}

void print_welcome(){
	printf("-----------------------------------------------------------------\n");
	printf("                            Welcome!                             \n");
	printf("  You will be presented with 30 flags of the form DogeCTF{flag}  \n");
	printf("   You'll have to twist your wrist a little and scramble them    \n");
	printf("                   like Migos to get the flag!                   \n");
	printf("          Before you go take this: %d, you'll need it          \n", getpid());
	printf("-----------------------------------------------------------------\n");
	printf("\n\n\n");
}

int main(){
	print_welcome();
	int win = play_game();
	if(win){
		print_flag();
	}else{
		print_loss();
	}
	return 0;
}
