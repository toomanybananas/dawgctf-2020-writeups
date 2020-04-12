# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 20:56:17 2020

@author: pleoxconfusa
"""
import math

n = 960242069
e = 347
d = 5497883 #pretend this doesn't exist
p = 151
q = 6359219


#lcm of p-1 and q-1
phi = abs((p-1)*(q-1)) // math.gcd(p-1,q-1)
#e*d=1 mod phi. we have to find d.
#we must first find the totient of phi.
#The totient is the size of the largest 
#field generated under modulus phi.


def totient(n):
    amount = 0  
    for k in range(1, n + 1):
        if not k % (n // 100):
            print(k/(n//100),'% done.\n')
        if math.gcd(n, k) == 1:
            amount += 1
    return amount

#d = e^{totient(phi)-1} % phi
#d_1 = pow(e,totient(phi)-1,phi)
#print(d,d_1)


#this is the original puzzle
ct=[295161774,843462311,530533280,787183046,851931432,770121847,770121847,346046109,616062960,118512782,321883599,860892522,657690757,725148418,346046109,137112544,118512782,563542899,185391473,770057231,790750242,556994500,202294479,530533280,110489031,231979042,657690757,137112544,683778547,227720616,546341739,788320338,259677897,731220302,725148418,475241234,271790171,202294479,530533280,405302860,616062960,923405109,851931432,289862692,945606673,625021022,725148418,70699533,221180981,278854535,770057231,584652061,508395428,185391473,657690757,284629213,321883599,636253020,221180981,271790171,271790171,851931432,923405109,559148396,13976622,475241234]

to_print = ""
for c in ct:
    val = pow(c,d,n)
    to_print += chr(val) 
    
print(to_print)