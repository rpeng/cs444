; Reference assembly for P.B.s

section .data
; VTable
V~P.B:
  dd n~P.B
  dd V~P.A
  ; methods
  dd m~P.B~f
  dd m~P.A~g~@int
  dd m~P.B~h

n~P.B:
  db 3, "P.B"

section .bss
; Statics

section .text
; Methods
mc~P.B:
  push ebp
  mov ebp, esp
  ; constructor body
  leave
  ret

m~P.B~h:
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

m~P.B~f:
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

; Symbol Exports
global mc~P.B
global V~P.B
global m~P.B~f
global m~P.B~h
global n~P.B

; Symbol Imports
extern V~P.A
extern m~P.A~g~@int
