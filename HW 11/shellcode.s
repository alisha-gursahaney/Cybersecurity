; shellcode.s

global shellcode

mysyscall:
    jmp shellcode
string:
    db "Alisha, your grade on this assignment is an A "
    
shellcode:    
    xor eax, eax
    mov al, 1
    mov edi, eax
    lea rsi, [rel string]
    sub byte [rsi+45],22
    xor edx, edx
    mov dl, 46
    syscall
    mov al, 60
    xor edi, edi
    syscall