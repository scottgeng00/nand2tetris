// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

	@R1
	D=M			//copy x2 to addr i
	@i			
	M=D
	
	@R2			//initialize product as 0
	M=0

(LOOP)
	@i
	D=M
	@END		//check if i <= 0, exit loop if so
	D;JLE
	
	@R0
	D=M			//product += x1
	@R2
	M=M+D
	
	@i
	M=M-1
	
	@LOOP
	0;JMP
	
(END)
	@END
	0;JMP

