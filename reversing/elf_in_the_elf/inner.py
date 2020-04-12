from pwn import *
context.arch = "amd64"

code = """
    lea rbx, [rip + flag]
    xor rcx, rcx
    loop:
        xor BYTE PTR [rbx + rcx], 0x69
	inc rcx
    exit:
        cmp rcx,27
        jne loop

    mov rdx,26
    lea rsi, [rip+flag]
    mov rdi,1
    mov rax,1
    syscall
    mov rdi,0
    mov rax,60
    syscall
flag: .ascii "\\x2D\\x08\\x1E\\x0E\\x2A\\x3D\\x2F\\x12\\x1A\\x1E\\x29\\x0E\\x36\\x58\\x07\\x36\\x1D\\x01\\x5A\\x36\\x0F\\x05\\x29\\x0E\\x14\\x63"

"""
code = asm(code)
elf = make_elf(code)
open("inner", 'wb').write(elf)
