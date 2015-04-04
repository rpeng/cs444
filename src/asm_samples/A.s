section .data
; Data section
; Virtual table of A
global V~P.A
V~P.A:
  dw n~P.A         ; pointer to name of class of A
  dw 0             ; pointer to superclass of A (none)
  dw m~P.A~f       ; pointer to A.f
  dw m~P.A~g~@int  ; pointer to A.g(int)
  
; Name for class P.A
global n~P.A
n~P.A:
  db 3, "P.A"

section .bss
; Uninitialized variables (static vars)

section .text

; Methods of A
global mc~P.A
mc~P.A:  ; constructor
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

global m~P.A~f
m~P.A~f:  ; A.f()
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

global m~P.A~g~@int
m~P.A~g~@int:  ; A.g(int)
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

