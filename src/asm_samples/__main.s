section .text

global _start

putch:  ; puts al to stdout
  mov [char], al ; save the low order byte in memory
  mov eax, 4     ; sys_write system call
  mov ecx, char  ; address of bytes to write
  mov ebx, 1     ; stdout
  mov edx, 1     ; number of bytes to write
  int 0x80
  mov eax, 0     ; return 0
  ret

_start:
  mov eax, 'A'
  call putch
  mov eax, 1
  mov ebx, 0
  int 0x80


section .data

char:
  dd 0
