# Ocean Boutique

## Building

Run `make`

## Solving

Intended solution path:
1. Reverse the conditions in main()
2. Figure out loosely how input works
3. Find the table of opcodes
4. Reverse them
5. Find the stock table
6. Pull out the data
7. Try a solution, realize weight is a thing
8. Look at the stock table for a couple minutes, then find the solution that was
   light enough to be valid. (This wasn't intended to be a knapsack problem, it
    should have been pretty obvious once you could view the stock table data.)
9. Generate your transaction
10. Somewhere along the way, figure out how to trigger receipt printing
11. Win!

## Sample solution

See solve.txt, it has the transcript of my test solution

## Files

I've provided the binary, the original source code `ocean_boutique.c`, as well
as a sample transaction that solves the challenge in `solve.txt`.
