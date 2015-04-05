; Reference assembly for A.java

section .data
; VTable
V~P.A:
  dd n~P.A
  dd 0
  ; methods
  dd m~P.A~f
  dd m~P.A~g~@int

n~P.A:
  db 3, "P.A"

section .bss
; Statics
s~P.A~i resd 1

section .text
; Methods
mc~P.A:
  push ebp
  mov ebp, esp
  ; constructor body
  leave
  ret

m~P.A~f:
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

m~P.A~g~@int:
  push ebp
  mov ebp, esp
  ; method body
  leave
  ret

; Symbol Exports
global V~P.A
global mc~P.A
global n~P.A
global m~P.A~g~@int
global m~P.A~f

; Symbol Imports
