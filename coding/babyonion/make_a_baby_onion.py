#!/usr/bin/python3
from base64 import b64encode
import sys

def main():
    if not (len(sys.argv) > 1 and len(sys.argv) < 3):
        print(f"[!] Incorrect usage. { sys.argv[0] } <flag>") 
    else:
        flag = sys.argv[1]
        tmp = flag
        for i in range(15):
            #print(f"tmp: {tmp}")
            tmp1 = b64encode(tmp.encode('ascii'))
            #print(f"b64 tmp: {tmp1}")
            tmp2 = tmp1.hex()
            tmp = tmp2
            #print(len(tmp))
        print(tmp)
            
if __name__ == "__main__":
    main()
