#pip install git+git://github.com/jameslyons/pycipher

import base64
import random
import string
import pycipher
import signal
TIMEOUT = 5

print "-----------------------------------------------------------------------"
print "Welcome to DiffSpot, a new Spot the Differnce Game sponsored by DawgSec"
print "          You'll be presented with a variety of encoded data,          "
print "              all of which will be of the form DogeCTF{}               "
print "Possible ciphers include:"
print "- rot13"
print "- rot16"
print "- base64"
print "- base32"
print "- base16"
print "- atbash"
print "- affine with b=6, a=9"
print "- railfence with key=3"
print "         Your job is to decode the flag and send it back to us         "
print "                     Seems easy enough right?                          "
print "-----------------------------------------------------------------------"

flag = "DawgCTF{w@iT_th3y_w3r3_d1ff3rent?!}"

def input():
	signal.alarm(TIMEOUT)
	foo = raw_input()
	signal.alarm(0)
	return foo

def rot13(cleartext):
	rot13 = string.maketrans(
	    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
	    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
	print string.translate(cleartext, rot13)

def rot16(cleartext):
	rot16 = string.maketrans(
	    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
	    "QRSTUVWXYZABCqrstuvwxyzabcDEFGHIJKLMNOPdefghijklmnop")
	print string.translate(cleartext, rot16)

def dobase64(cleartext):
	print base64.b64encode(cleartext)

def dobase16(cleartext):
	print base64.b16encode(cleartext)

def dobase32(cleartext):
	print base64.b32encode(cleartext)

def doatbash(cleartext):
	print pycipher.Atbash().encipher(cleartext, keep_punct=True)

def doaffine(cleartext):
	print pycipher.Affine(9,6).encipher(cleartext, keep_punct=True)

def dorailfence(cleartext):
	print pycipher.Railfence(3).encipher(cleartext, keep_punct=True)

correct = 1

for i in range(0, 100):
	str = "DogeCTF{"
	str += ''.join([random.choice(string.ascii_letters) for n in xrange(32)])
	str += "}"
	choice = random.randint(1, 8)
	if choice == 1:
		rot13(str)
	if choice == 2:
		rot16(str)
	if choice == 3:
		dobase64(str)
	if choice == 4:
		dobase32(str)
	if choice == 5:
		str = str.upper()
		doatbash(str)
	if choice == 6:
		str = str.upper()
		doaffine(str)
	if choice == 7:
		str = str.upper()
		dorailfence(str)
	if choice == 8:
		dobase16(str)
	user_input = input()
	if user_input != str:
		print "WRONG USER INPUT:"
		print user_input
		print "WRONG ORIGINAL STRING:"
		print str
		correct = 0
		break

if correct == 0:
	print "Maybe these are all the same..."
else:
	print "Dang you're good, here\'s your flag: " + flag
