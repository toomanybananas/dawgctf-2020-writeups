from pwn import *
from subprocess import Popen, PIPE
import ctypes

LIBC = ctypes.cdll.LoadLibrary('/lib/x86_64-linux-gnu/libc.so.6')

#proc = process("./strfry")
proc = remote("ctf.umbccd.io", 5100)
pid = proc.recvuntil(",").split()[-1]
pid = pid[:-1]
time_null = LIBC.time(0)
sop = process(["./strfry_sol", str(time_null), pid])
for i in range(0, 30):
	fake_flag = proc.recvuntil("}").split()[-1]
	print fake_flag
	sop.sendline(fake_flag)
	sol = sop.recvline()
	print "Solution: " + sol
	proc.send(sol)

proc.interactive()
