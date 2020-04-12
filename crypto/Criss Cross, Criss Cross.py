# -*- coding: utf-8 -*-
"""

Hint: Look up the chosen plaintext attack and try using your new pad function.

@author: pleoxconfusa
"""

import socket

#some potentially useful functions
def pad_equal(a,b):
    diff = len(a)-len(b)
    if diff > 0:
        b += b"\0" * diff
    else:
        a += b"\0" * -diff
    return a,b
    
def xor_bytes(a,b):
    return bytes(x ^ y for x, y in zip(a, b))

BLOCK_SIZE = 16
pad = lambda s: s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) % BLOCK_SIZE) * b'\0'


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13375)
sock.connect(server_address)

#available methods: flg, enc, dec.

msg = 'tst'.encode()
sock.sendall(msg)
tst = sock.recv(1024)
print(tst)#not decoded, because now the oracle sends encrypted bytes.

mac = tst[:BLOCK_SIZE]
txt = tst[BLOCK_SIZE:]

msg = b'vfy:' + mac + pad(txt) + xor_bytes(mac,txt[:16]) + txt[16:] #sanity double check
sock.sendall(msg)
res = sock.recv(1024)
print(res) 
    
sock.close()