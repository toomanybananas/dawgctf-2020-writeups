# DEFCON Practice - 500 points

## Solution

* Find out what challenge this PCAP is an exploit of, read a writeup, determine that it is writing/leaking data by modifying gears
  * Alternatively, you can just guess that's what happening since the first 8 bytes written looks like a memory address (0x7f.....)
* Extract the written data and examine it
* First part is a ROP chain (don't need to actually resolve the gadgets to solve this), it looks like a standard mprotect() chain
* Next part is shellcode with some light anti disassembly
* Shellcode reads a filename, decrypts it, opens it, sends the contents back encrypted
* Encryption algorithm used is RC4 with an intentional bug: in between the two encryptions, the state is not reset but the counter is. PyCrypto, CyberChef, and all other libs annoyingly correctly decrypt the filename but not the contents
* Furthermore, the shellcode derives the key from two things: an int send over the connection (unencrypted) and something that is part of the binary. So you need to actually grab the binary so solve this challenge
* Write your own RC4 implemtnation (or copy and paste + modify) then decrypt the bit at the end of the PCAP
