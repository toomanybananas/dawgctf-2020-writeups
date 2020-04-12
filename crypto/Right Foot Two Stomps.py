# -*- coding: utf-8 -*-
"""

Hint: Look up the chosen ciphertext attack.  

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


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13372)
sock.connect(server_address)

#available methods: flg, enc, dec.

msg = 'flg'.encode()
sock.sendall(msg)
ct = sock.recv(1024)
print(ct)

msg = b'dec:' + ct + ct #very simple solution.
sock.sendall(msg)
dec = sock.recv(1024)
print(dec) 
    
sock.close()