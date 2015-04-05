extern m~P.A~g~@int
extern V~P.A

section .data

; Data section
; Virtual table of B
V~P.B:
  dd n~P.B         ; pointer to name of class of B
  dd V~P.A         ; pointer to superclass of B
  dd m~P.B~f       ; pointer to B.f (override)
  dd m~P.A~g~@int  ; pointer to A.g(int)
  dd m~P.B~h       ; pointer to B.h

; Name for class P.B
n~P.B:
  db 3, "P.B"

section .bss
; Uninitialized variables (static vars)

section .text

; Methods of B
global mc~P.B
mc~P.B:  ; constructor
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

global m~P.B~f
m~P.B~f:  ; A.f()
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

global m~P.B~h
m~P.B~h:  ; B.h
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret
