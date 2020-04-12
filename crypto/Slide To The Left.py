# -*- coding: utf-8 -*-
"""

Hint: Look up the chosen ciphertext attack for cbc malleability

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

server_address = ('localhost', 13373)
sock.connect(server_address)

#available methods: flg, enc, dec.

msg = 'flg'.encode()
sock.sendall(msg)
ct = sock.recv(1024)
print("ct:" , ct)
print(1)
msg = b'dec:' + ct[:-16] #to get the first block decrypted
print(2)
sock.sendall(msg)
print(3)
dec1 = sock.recv(1024)
print("dec1:", dec1)
msg = b'dec:' + ct[16:] #very simple solution to get everything after the first block decrypted
sock.sendall(msg)
dec2 = sock.recv(1024)
print("dec2:", dec2)
print(dec1[:16]+dec2) 
    
sock.close()