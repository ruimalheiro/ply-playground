.data 
newline: .asciiz "\n" 
FALSE: .float 0.0 
TRUE: .float 1.0 
FL0: .float 3.0 
FL1: .float 2.3 
.text
li $s0 5 
li $t0 0 
sgt $t0 $s0 $t0 
bge $t0 1 L0 
j L1 
L0: 
li $t0 4 
add $s1 $t0 $s0 
move $a0 $s1 
li $v0 1 
syscall 
li $v0 4 
la $a0 newline 
syscall 
L1: 
lwc1 $f20 FL0 
lwc1 $f0 FL1 
mul.s $f21 $f0 $f20 
mov.s $f12 $f21 
li $v0 2 
syscall 
li $v0 4 
la $a0 newline 
syscall 
li $v0, 10 
syscall 
