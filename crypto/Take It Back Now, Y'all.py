# -*- coding: utf-8 -*-
"""

Hint: Wait really? Uhm. Okay.  Just change the msg to say 'flg'.

@author: pleoxconfusa
"""

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('crypto.ctf.umbccd.io', 13370)
sock.connect(server_address)

#available methods: flg, tst.


msg = 'flg'


sock.sendall(msg.encode())
data = sock.recv(1024)
print(data.decode())
    
sock.close()