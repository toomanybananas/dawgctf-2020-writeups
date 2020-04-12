from pwn import *

#p = process("./miracle_mile")
p = remote("ctf.umbccd.io", 5300)

print p.recvuntil("-----------------------------------------")
print p.recvuntil("-----------------------------------------")
while(1):
	sol = p.recvuntil(" ")
	if "Dang" in sol:
		break
	p.recvuntil(" ")
	dist = p.recvuntil(" ")
	p.recvuntil("in ")
	time = p.recvuntil(" ")
	p.recvuntil("? ")

	hour, min, sec = [int(x) for x in time.split(':') if x.strip()]
	total = (hour*60*60) + (min*60) + sec
	sol_min = int((total/float(dist)) / 60)
	sol_sec = int((total/float(dist)) % 60)

	print str(sol_min) + ":" + str(sol_sec)

	p.sendline(str(sol_min) + ":" + str(sol_sec))

p.interactive()
