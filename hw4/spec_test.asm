; Test 1: Load Constant (A=82, B=352, C=346)
; Expected: 0x52, 0xB0, 0xD0, 0x0A
LOAD 352 346

; Test 2: Read Memory (A=19, B=511, C=112, D=71)
; Expected: 0x93, 0xFF, 0x80, 0x83, 0x23, 0x00
READ 511 112 71

; Test 3: Write Memory (A=31, B=27, C=148, D=883)
; Expected: 0x9F, 0x0D, 0xA0, 0x64, 0x6E, 0x00
WRITE 27 148 883

; Test 4: BSWAP (A=22, B=810, C=188)
; Expected: 0x16, 0x95, 0xE1, 0x05
BSWAP 810 188
