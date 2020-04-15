#!/usr/bin/python3
from base64 import b64decode
import sys

def main():
    if not (len(sys.argv) > 1 and len(sys.argv) < 3):
        print(f"[!] Incorrect usage. { sys.argv[0] } <flag file>") 
    else:
        with open(sys.argv[1], 'r') as f:
            flag = f.read()
        while 'DawgCTF' not in flag:
            flag = bytes.fromhex(flag)
            flag = b64decode(flag).decode('ascii')
        print(f"flag?: {flag}")
            
if __name__ == "__main__":
    main()
