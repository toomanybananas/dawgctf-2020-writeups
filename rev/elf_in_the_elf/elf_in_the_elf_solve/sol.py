import os

fout = open("out","wb")
for i in xrange(4408):
    print i
    fname = "elfs/elf_%d"%i
    os.system("objdump -M intel -d %s | grep -A40 '<math>:' > tmpout"%fname)
    code = open("tmpout","rb").read()
    code = code[:code.index('ret')+3]
    #print code
    code = code.split('\n')
    correctj = [j for j in xrange(len(code)) if "[rbp-0x1]" in code[j]][0]
    correct = int(code[correctj].split(',')[-1].strip(), 16)
    code = code[correctj:]
    #print ""
    #print hex(correct)
    opl = [l for l in code if "xor" in l or "add" in l or "sub" in l]
    if len(opl) == 0:
        fout.write(chr(correct))
        fout.flush()
        continue
    opl = opl[0]
    #print opl
    opconst = int(opl.split(',')[-1].strip(), 16)
    #print hex(opconst)
    sol = None
    if "xor" in opl:
        sol = (correct ^ opconst)&0xff
    elif "add" in opl:
        sol = (correct - opconst)&0xff
    elif "sub" in opl:
        sol = (correct + opconst)&0xff
    print hex(sol)
    fout.write(chr(sol))
    fout.flush()
