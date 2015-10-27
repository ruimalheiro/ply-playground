PLY Playground
==========================================

This is a simple academic project that explores the basics of PLY. This compiler will generate MIPS assembly code that can be run using MARS MIPS Simulator.

----
#### Instructions:
* In order to run it, Python 2.7 must be installed.
* Run command: "python compiler.py 'input'" , where "input" is the name of the file that contains the source code.
* A file named "output.asm" will be generated and it can be used within the MARS MIPS Simulator.

----
#### "Foo" Language Rules:
* All commands end in ";".
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


- The first mistake is related with the variable "x". Adding 3.0 to "x" will lead to a type error because "x" was initialized as an Integer.
- The second mistake is related with scope violation. The variable "y" was initialized within the "if" scope and shall only be accessible within the scope where it was created or within the children scopes.
