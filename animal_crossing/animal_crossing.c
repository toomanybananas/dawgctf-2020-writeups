#include <stdio.h>
#include <unistd.h>
#include <string.h>

#define ITEMS_FOR_SALE 6
#define BAG_SIZE 5

unsigned int bells = 8500;

struct item{
	char name[20];
	char desc[50];
	unsigned int price;
	unsigned int qty;
	int num;
};

struct item sale_items[ITEMS_FOR_SALE];
struct item my_items[BAG_SIZE];
unsigned int num_items = 4;
int valid_items[BAG_SIZE] = {1, 1, 1, 1, 0};

char welcome_str[] = "Welcome!\nHow can I help you today?\n";
char leave_str[] = "Well then, please don\'t hesitate to\nask if you need assistance!\n";
char sale_str[] = "Excellent purchase!\nYes, thank you for the bells\n";
char sale_str_1[] = "Here\'s what we have to sell today.\n";
char cant_afford[] = "I\'ll buy it!\nThank you for your purcha--\nOh! You, ah, don\'t have enough\nmoney in your pockets.\nOur shop doesn't offer a line of credit,\nso please come back when\nyou have more money.\n...money!\n\n";
char sure[] = "Sure! How about if I offer you\n";
char thanks[] = "Thank you! Please come again!\n\n";
char sell_str[] = "Of course! What exactly are you\noffering?\n";
char bag_full[] = "Thank you for your purcha-\nWhoa! You\'re already carrying so\nmany things!\nMaybe you can come back after you\nmake room in your pockets.\n";


void print_string(char* str, int len){
        for (int i = 0; i < len; ++i) {
                printf("%c", str[i]);
                usleep(15000);
        }
}

void setup_sale_items(){
	char item_names[][20] = {"flimsy net",
				"tarantula",
				"slingshot",
				"sapling",
				"cherry",
				"flag"};
	char item_desc[][50] = {"a great way to catch bugs!",
				"I hate spiders!",
				"the closest thing you can get to a gun",
				"plant a tree!",
				"eh it beats pears",
				"DogeCTF{t0m_n00k_c@pit4l1st_$cum}"};
	unsigned int item_price[] = {400, 8000, 900, 640, 400, 420000};
	unsigned int item_qty[] = {0, 0, 0, 0, 0, 0};
	int item_num[] = {1, 2, 3, 4, 5, 6};
	for(int i = 0; i < ITEMS_FOR_SALE; i++){
		strcpy(sale_items[i].name, item_names[i]);
		strcpy(sale_items[i].desc, item_desc[i]);
		sale_items[i].price = item_price[i];
		sale_items[i].qty = item_qty[i];
		sale_items[i].num = item_num[i];
	}
}

void setup_my_items(){
	char item_names[][20] = {"flimsy axe",
				"olive flounder",
				"slingshot",
				"flimsy shovel",
				};
	char item_desc[][50] = {"chop chop chop",
				"it\'s looking at me funny",
				"the closest thing you can get to a gun",
				"for digging yourself out of debt",
				};
	unsigned int item_price[] = {800, 800, 900, 800};
	unsigned int item_qty[] = {1, 2, 1, 1};
	int item_num[] = {7, 8, 3, 9};
	int i;
	for(i = 0; i < num_items; i++){
		strcpy(my_items[i].name, item_names[i]);
		strcpy(my_items[i].desc, item_desc[i]);
		my_items[i].price = item_price[i];
		my_items[i].qty = item_qty[i];
		my_items[i].num = item_num[i];
	}
	for(; i < BAG_SIZE; i++){
		my_items[i].price = -1;
		my_items[i].qty = -1;
		my_items[i].num = -1;
	}
}

void print_welcome(){
	printf("Timmy: ");
	print_string(welcome_str, strlen(welcome_str));
}

void exit_game(){
	printf("Timmy: ");
	print_string(leave_str, strlen(leave_str));
}

void make_sale(int item_num){
	printf("Timmy: ");
	print_string(sale_str, strlen(sale_str));
	int item_index = -1;
	for(int i = 0; i < BAG_SIZE; i++){
		if(item_num == my_items[i].num && valid_items[i]){
			item_index = i;
		}
	}
	if(item_index == -1){
		for(int i = 0; i < BAG_SIZE; i++){
			if(!valid_items[i]){
				item_index = i;
				break;
			}
		}
		strcpy(my_items[item_index].name, sale_items[item_num-1].name);
		strcpy(my_items[item_index].desc, sale_items[item_num-1].desc);
		my_items[item_index].price = sale_items[item_num-1].price;
		my_items[item_index].num = item_num;
		num_items++;
		valid_items[item_index] = 1;
	}else{
		my_items[item_index].qty += 1;
	}
	bells = bells - sale_items[item_num-1].price;
}

void sale(){
	int choice = 0;
	printf("%d bells\n", bells);
	printf("Timmy: ");
	print_string(sale_str_1, strlen(sale_str));
	for(int i = 0; i < ITEMS_FOR_SALE; i++){
		printf("%d. %s - %d bells\n", i+1, sale_items[i].name, sale_items[i].price);
	}
	scanf("%d", &choice);
        while((getchar()) != '\n');
	printf("\n");
	if(choice > ITEMS_FOR_SALE || choice < 1){
		printf("Invalid Choice\n");
		return;
	}
	if(bells - sale_items[choice-1].price > bells){
		print_string(cant_afford, strlen(cant_afford));
		return;
	}
	make_sale(choice);
}

void sell_item(int choice){
	printf("Timmy: ");
	printf("A %s!\n", my_items[choice].name);
	print_string(sure, strlen(sure));
	printf("%d Bells?\n", my_items[choice].price);
	my_items[choice].qty -= 1;
	bells += my_items[choice].price;
	if(my_items[choice].qty == 0){
		valid_items[choice] = 0;
		num_items -= 1;
	}
	print_string(thanks, strlen(thanks));
}

void sell(){
	int choice = 0;
	print_string(sell_str, strlen(sell_str));
	for(int i = 0; i < BAG_SIZE; i++){
		if(valid_items[i]){
			printf("%d. %s - %s Price: %d bells\n", i+1, my_items[i].name, my_items[i].desc, my_items[i].price);
		}
	}
	scanf("%d", &choice);
        while ((getchar()) != '\n');
	printf("\n");
	if(choice < 1 || choice > BAG_SIZE || !valid_items[choice-1]){
		printf("Invalid Choice\n");
		return;
	}
	sell_item(choice-1);
}

void store(){
        while(1){
                int choice = 0;
                printf("1. I want to sell\n");
                printf("2. What's for sale?\n");
                printf("3. See you later.\n");
                printf("Choice: ");
                scanf("%d", &choice);
                while ((getchar()) != '\n');
                printf("\n");
		switch(choice){
			case 1:
				sell();
				break;
			case 2:
				if(num_items >= BAG_SIZE){
					print_string(bag_full, strlen(bag_full));
				}else{
					sale();
				}
				break;
			case 3:
				exit_game();
				return;
		}
	}
}

int main(){
        setvbuf(stdout, 0, _IONBF, 0);
	setup_sale_items();
	setup_my_items();
	print_welcome();
	store();
	return 0;
}
