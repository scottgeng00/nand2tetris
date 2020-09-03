// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
	
	@offset
	M=-1				//this is the last filled screen address, as on offset from @SCREEN. -1 means none filled
	
	@clear_const
	M=0
	@fill_const
	M=-1
	
	@SCREEN
	D=A
	@loc
	M=D
	
	

(LOOP)

	@KBD
	D=M				//get keyboard input
	
	@CLEAR
	D;JEQ			//if 0 (no input) clear
	
	@FILL
	D;JNE			//else fill
	
	@LOOP
	0;JMP
	
	
(CLEAR)
	@offset
	D=M
	@LOOP			//if offset is <0, screen already clear, go back to original loop
	D;JLT
	
	@SCREEN
	D=A				//put base address into D
	@offset
	D=D+M			//add the offset to base address
	@loc
	M=D				//store new address in RAM
	
	@clear_const
	D=M
	
	@loc 			//get screen location from memory
	A=M				
	M=D				//write the constant to the screen to clear
	
	@offset
	M=M-1
	
	@CLEAR
	0;JMP
	

(FILL)

	@offset
	D=M+1
	@8192
	D=A-D			//offset+1=8192=A when completelty filled
	
	@LOOP
	D;JEQ
	
	@SCREEN
	D=A 
	@offset
	D=D+M
	@loc
	M=D				//store new address in RAM
	
	
	@fill_const
	D=M
	
	@loc 			//get screen location from memory
	A=M				
	M=D				//write the constant to the screen to clear
	
	@offset
	M=M+1
	
	@FILL
	0;JMP
	
	