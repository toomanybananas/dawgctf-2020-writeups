from pwn import *
import pycipher
import base64

if "rem" in sys.argv:
	proc = remote("ctf.umbccd.io", 5200)
else:
	proc = process(["python", "./spotthedifference.py"])

proc.recvuntil("-----------------------------------------------------------------------")
proc.recvuntil("-----------------------------------------------------------------------")

def trycurlybracelower(enc):
        rot13 = string.maketrans(
            "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm",
            "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz")
        dec = string.translate(enc, rot13)
	if dec.find("DogeCTF") >= 0:
		print "ROT13 found"
		print dec
		return dec
        rot16 = string.maketrans(
            "QRSTUVWXYZABCqrstuvwxyzabcDEFGHIJKLMNOPdefghijklmnop",
            "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz")
        dec = string.translate(enc, rot16)
	if dec.find("DogeCTF") >= 0:
		print "ROT16 found"
		print dec
		return dec
	print "Fuck it didn\'t work in lowercase"

def trycurlybraceupper(enc):
	dec = pycipher.Atbash().decipher(enc, keep_punct=True)
	if("DOGECTF" in dec):
		print "Atbash found"
		print dec
		return dec
	dec = pycipher.Affine(9,6).decipher(enc, keep_punct=True)
	if("DOGECTF" in dec):
		print "Affine found"
		print dec
		return dec
	print "Fuck it didn\'t work in uppercase"

def tryrailfence(enc):
	dec = pycipher.Railfence(3).decipher(enc, keep_punct=True)
	if("DOGECTF" in dec):
		print "Railfence found"
		print dec
		return dec
	print "Fuck it didn\'t work"

def dobase64(enc):
	print "Base64 found"
	dec = base64.b64decode(enc)
	print dec
	return dec

def dobase32(enc):
	print "Base32 found"
	dec = base64.b32decode(enc)
	print dec
	return dec

def dobase16(enc):
	print "Base16 found"
	dec = base64.b16decode(enc)
	print dec
	return dec

enc = proc.recvline()

for i in range(0,100):
	enc = proc.recvline()
	if "WRONG" in enc:
		proc.interactive()
	enc = enc.strip()
	print enc
	print enc[-1]
	dec = ""
	if enc[1].isupper() & (enc[-1] == "}"):
		dec = trycurlybraceupper(enc)
	elif enc[-1] == "}":
		dec = trycurlybracelower(enc)
	elif "}" in enc:
		dec = tryrailfence(enc)
	elif enc[-2:] == "==":
		dec = dobase32(enc)
	elif enc[-1] == "=":
		dec = dobase64(enc)
	else:
		dec = dobase16(enc)
	proc.sendline(dec)

proc.interactive()
