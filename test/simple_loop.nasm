bits 64
org 0xb0000000

mov ecx, 0x3290
loop:
mov dword [esi], ecx
dec ecx
jnz loop
