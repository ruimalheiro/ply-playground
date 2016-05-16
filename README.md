PLY Playground
==========================================

This is a simple academic project that explores the basics of PLY. This compiler will generate MIPS assembly code that can be run using MARS MIPS Simulator.

----
#### Instructions:
* In order to run it, Python 2.7 must be installed.
* Run command: `python compiler.py 'input'` , where `input` is the name of the file that contains the source code.
* A file named `output.asm` will be generated and it can be used in MARS MIPS Simulator.

----
#### "Foo" Language Rules:
* All commands end in `;`.
* The variables are global, and they keep the type that was assigned to them when they were initialized.

----
#### Valid program example:
	x <- 5;

	if x > 0 then
	begin
		z <- 4 + x;
		print z;
	end;

	y <- 3.0;
	p <- 2.3 * y;

	print p;

----
#### Invalid program example:

	x <- 5;

	if x > 0 then
	begin
		z <- 4 + x;
		print z;
		y <- 3.0 + x;
	end;

	p <- 2.3 * y;

	print p;


- The first mistake is related with the variable `x`. Adding `3.0` to `x` will lead to a type error because `x` was initialized as an Integer.
- The second mistake is related with scope violation. The variable `y` was initialized within the `if` scope and shall only be accessible within the scope where it was created or within the children scopes.


----
#### MIPS code generated from the previous valid example:

	.data
	newline: .asciiz "\n"
	FALSE: .float 0.0
	TRUE: .float 1.0
	FL0: .float 3.0
	FL1: .float 2.3
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
