section .text
global _start

_printnum:
  push ebp
  mov ebp, esp

  push dword [ebp+12]
  add [esp], dword '0'
  mov ecx, esp

  mov edx, 1
  mov ebx, 1
  mov eax, 4
  int 0x80

  mov esp, ebp
  pop ebp
  ret

_start:
  ; mov edx, len
  ; mov ecx, msg
  ; mov ebx, 1
  ; mov eax, 4
  ; int 0x80

  push dword 1
  call _printnum

  mov eax, 1
  int 0x80


section .data
msg db "Hello, world!", 0xa
len equ $ - msg

