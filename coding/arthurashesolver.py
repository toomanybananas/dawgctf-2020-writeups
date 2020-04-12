# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:46:02 2020

@author: pleoxconfusa
"""


import socket
import binascii


flag = ""


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('arthurashe.ctf.umbccd.io', 8411)
sock.connect(server_address)

prompt = sock.recv(1024)
while prompt:
    prompt = prompt.decode("utf-8")
    
    
    
    if prompt[-1] == '?':
        sock.sendall('Y'.encode())
    elif prompt[-1] == '!':
        break
    elif prompt[-1] == '.':
        msg = ''
        
        score_tuple = prompt.split()[-1][:-1].split('-')
        
        score = []
        
        for index in score_tuple:
            if index == 'love':
                score.append(0)
            elif index == 'game':
                score.append(50)
            elif index == 'set':
                score.append(6)
            else:
                score.append(int(index))
                
        if score[0] > score[1]:
            msg = '0'
        else:
            msg = '1'
        
        flag += msg
    
    
        sock.sendall(msg.encode())
        
    prompt = sock.recv(1024)
    

sock.close()

print(binascii.unhexlify('%x' % int(flag,2)))