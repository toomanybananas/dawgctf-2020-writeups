BINS=ocean_boutique
CC=gcc
STRIP=strip
CFLAGS=-Wall -Wextra -Wno-unused-parameter -fno-inline

all: $(BINS)

.PHONY: all

ocean_boutique: ocean_boutique.c
	$(CC) $(CFLAGS) "$<" -o "$@"
	$(STRIP) "$@"

clean:
	rm -f *.o $(BINS)

.PHONY: clean
