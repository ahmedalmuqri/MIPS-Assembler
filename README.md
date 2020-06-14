# MIPS-Assembler
Translates most of MIPS Assembly language Instructions  to Machine language.

As a CPU is running, it must fetch instructions from RAM to determine what computations to
perform. In the MIPS instruction set architecture (ISA) instructions are stored as 32-bit values. The
representation of MIPS instructions as these 32-bit values is called machine code, and the symbolic
representation of the instructions is called assembly code.
An assembler is a program which translates assembly code into its equivalent machine code. In almost
all cases this translation is a one-to-one mapping, and this code here implements a
MIPS assembler. 

The input to assembler will be a .asm (assembly) file. Each line is formatted as

[ label :] instruction arg0 [ arg1 ] [ arg2 ] [# comment ]
Where fields in brackets are optional – not every line has a label or comment, and not every instruction
has three arguments. This assembler figures out which arguments are provided for any
instruction. The assembler supports register arguments named following MIPS conventions
(e.g. $s0, $t1, $sp).
The instructions supported are:
• add
• addi
• sub
• and
• andi
• or
• ori
• xor
• xori
• nor
• sll
• sra
• srl
• slt
• slti
• beq
• bne
• j
• jal
• jr
• lw
• sw
• nop
