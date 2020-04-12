#define _POSIX_C_SOURCE 200809
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define OP_PUR 3
#define OP_TOTAL 8
#define OP_QTY 4
#define OP_PAY 6
#define OP_END 9

#define MAX_WEIGHT 1000

#define STATIC __attribute__ ((visibility ("hidden")))

struct stock_item {
	int item_id;
	char *title;
	int price;
	int weight;
};

STATIC struct stock_item STOCK_TABLE[] = {
	{
		.item_id = 1,
		.title = "Plush Retriever",
		.price = 133700,
		.weight = 8,
	},
	{
		.item_id = 30,
		.title = "Cruise Ship Ticket",
		.price = 1000,
		.weight = 3,
	},
	{
		.item_id = 10,
		.title = "Retriever Sticker",
		.price = 42,
		.weight = 1,
	},
	{
		.item_id = 2,
		.title = "Authentic Meme",
		.price = 1,
		.weight = 1,
	},
	{
		.item_id = 42,
		.title = "ACME Anvil",
		.price = 3133742,
		.weight = MAX_WEIGHT+1,
	},
	{
		.item_id = 77,
		.title = "Link of Blockchain",
		.price = 50000,
		.weight = 10,
	},
};

struct receipt_item {
	int quantity;
	struct stock_item *item;
	struct receipt_item *next;
};

struct line_item {
	int opcode;
	int immediate; // dollars * 100
	struct line_item *next;
};

struct transaction_state {
	bool total_pressed;
	bool print_receipt;
	int running_total; // Dollars * 100. Updated by opcodes, when items are added
	int paid_total;
	int next_qty; // Updated by quantity opcode, processed & reset on next item
	int total_weight;
};

STATIC struct line_item items = {0};

STATIC struct receipt_item receipt = {0};

STATIC struct transaction_state state = {
	.total_pressed = 0,
	.print_receipt = 0,
	.running_total = 0,
	.paid_total = 0,
	.next_qty = 1,
};

void error() {
	printf("error\n");
	exit(1);
}

void print_flag() {
	size_t size = 0;
	char *line = NULL;
	FILE *fp = fopen("flag.txt", "r");
	if (fp) {
		size = 0;
		getline(&line, &size, fp);
		fclose(fp);
	} else {
		line = strdup("DogeCTF{Flag is different on the server.}\n");
	}
	printf("%s", line);
	free(line);
}

STATIC void add_to_receipt(int quantity, struct stock_item *item) {
	struct receipt_item *r_item = malloc(sizeof(struct receipt_item));
	r_item->quantity = quantity;
	r_item->item = item;
	struct receipt_item *walk = &receipt;
	while (walk->next) walk = walk->next;
	walk->next = r_item;
}

STATIC void print_receipt() {
	struct receipt_item *walk = &receipt;
	printf("Receipt\n");
	while (walk->next) {
		walk = walk->next;
		printf("%d\t%s\n", walk->quantity, walk->item->title);
	}
	printf("\n");
}

STATIC void link_item(int opcode, int immediate) {
	struct line_item *item = malloc(sizeof(struct line_item));
	item->opcode = opcode;
	item->immediate = immediate;
	struct line_item *walk = &items;
	while (walk->next) walk = walk->next;
	walk->next = item;
#ifdef DEBUG
	printf("Got %d %d\n", opcode, immediate);
#endif
}

STATIC void get_input() {
	char buf[20];
	printf("Enter transaction.\n");

	for (size_t count = 0; count < 15; count++) {
		int opcode = 0;
		int immediate = 0;
		fgets(buf, sizeof(buf), stdin);

		char *walk = strtok(buf, " ");
		if (!walk) error();
		opcode = atoi(walk);

		walk = strtok(NULL, " ");
		if (!walk) error();
		immediate = atoi(walk);
		link_item(opcode, immediate);
		if (opcode == 9) {
			state.print_receipt = (immediate == 10);
			printf("\n");
			return;
		}
	}
	error();
}

STATIC struct stock_item *get_item(int immediate) {
	for (size_t i = 0; i < sizeof(STOCK_TABLE)/sizeof(STOCK_TABLE[0]); i++) {
		if (STOCK_TABLE[i].item_id == immediate) {
			return &STOCK_TABLE[i];
		}
	}
	error();
	return NULL; // shut up the compiler, which didn't detect the noreturn
}

STATIC void handle_purchase(int immediate) {
	struct stock_item *item = get_item(immediate);
	add_to_receipt(state.next_qty, item);
	state.running_total += item->price * state.next_qty;
	state.next_qty = 1;
	state.total_weight += item->weight;
}

STATIC void handle_instruction(int opcode, int immediate) {
	switch (opcode) {
		case OP_PUR:
			if (state.total_pressed) error();
			if (immediate < 0) error();
			handle_purchase(immediate);
			break;
		case OP_QTY:
			if (state.total_pressed) error();
			if (immediate < 0) error();
			state.next_qty = immediate;
			break;
		case OP_TOTAL:
			if (state.total_pressed) error();
			if (immediate != OP_TOTAL) error();
			state.total_pressed = true;
			break;
		case OP_PAY:
			if (!state.total_pressed) error();
			if (immediate < 0) error();
			if (immediate > state.running_total) error();
			state.paid_total += immediate;
			state.running_total -= immediate;
			break;
		case OP_END:
			break;
		default:
			error();
			break;
	}
}

STATIC void run_transaction() {
	printf("Processing transaction. Hopefully you remembered to:\n"
			"Purchase, Total, Pay, and End Transaction\n\n");
	struct line_item *walk = &items;
	while (walk->next) {
		walk = walk->next;
#ifdef DEBUG
		printf("Processing %d %d\n", walk->opcode, walk->immediate);
#endif
		handle_instruction(walk->opcode, walk->immediate);
	}
	if (state.print_receipt) {
		print_receipt();
	}
}

int main() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	printf("Welcome to the Ocean Boutique.\n"
		"Last year, y'all enjoyed the Snake Boutique, but I wanted to move closer to\n"
		"the C and find sequels by the shore, so I opened a new boutique.\n\n"
		"Your boss has directed you to purchase exactly 31337.42 of goods and keep the\n"
		"receipt. Don't forget to make sure it all fits in your suitcase!\n"
		"Thank you for using our self checkout, enjoy your vacation!\n\n");
	get_input();
	run_transaction();
	if (state.total_pressed &&
			state.print_receipt &&
			state.running_total == 0 &&
			state.paid_total == 3133742) {
		if (state.total_weight > MAX_WEIGHT) {
			printf(
					"You made it all the way to the airport, but your bags were too heavy. You are\n"
					"forced to leave an item behind. When you tell your boss the story, he signs you\n"
					"up for synergy training to help you plan better. Whomp whomp.\n"
			      );
			error();
		} else {
			print_flag();
		}
	} else {
		printf("Your boss is livid, you didn't follow his instructions. You're fired.\n");
		error();
	}

	return 0;
}
