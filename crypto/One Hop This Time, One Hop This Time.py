# -*- coding: utf-8 -*-
"""

Hint: Use your new xor_bytes function and read up on the flaws of one time pad.

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

server_address = ('crypto.ctf.umbccd.io', 13371)
sock.connect(server_address)

#available methods: flg, enc, dec.


msg = 'flg'.encode()
sock.sendall(msg)
flg = sock.recv(1024)

msg = b'enc:' + b'\0' * 50
sock.sendall(msg)
key = sock.recv(1024)

print(xor_bytes(flg,key)) #not decoded, because now the oracle sends encrypted bytes.
    
sock.close()