# **RISC-V Assembler**

This project is a simple RISC-V assembler that converts assembly instructions into binary machine code. It supports various instruction types, including **R-type, I-type, S-type, B-type, and J-type instructions**.

## **Features**
- Converts RISC-V assembly instructions to binary.
- Supports label handling and calculates offsets for branch and jump instructions.
- Reads input from a file and processes it into binary output.
- Implements individual instruction encoding for different types of instructions.

## **Instruction Types Supported**
- **R-type**: `add, sub, slt, srl, or, and`
- **I-type**: `lw, addi, jalr`
- **S-type**: `sw`
- **B-type**: `beq, bne, blt, bge, bltu, bgeu`
- **J-type**: `jal`

## **Usage**

### **Running the Assembler**
1. Place your RISC-V assembly code in a text file (e.g., `input.txt`).
2. Run the script and provide the filename when prompted:
   ```bash
   python assembler.py
3.	The script will output the corresponding binary machine code.

Example Input (input.txt)

addi x1, x0, 5
beq x1, x2, label
label:
add x3, x1, x2

Example Output

00000000010100000000000010010011
00000000001000001000000001100011
00000000001000001000000110110011

Code Overview

Registers

Defined in a dictionary, mapping RISC-V register names to their corresponding binary values.

Helper Functions
	•	to_binary(value, bits) → Converts an integer to binary representation with sign extension.
	•	rbin(), ibin(), sbin(), bbin(), jbin() → Functions to encode different instruction types into binary.
	•	take_input(filename) → Reads and processes assembly instructions from a file.
	•	typeof(command) → Determines the instruction type.
	•	calculate_offset_for_labels(commands) → Computes offsets for labels in branch and jump instructions.
	•	assemble(commands) → Converts assembly commands to binary.

Contributions
	•	Arjun & Ayush – Implemented primary instruction type functions and typeof() function.
	•	Nirmit Jain – Developed input handling and binary helper functions.
	•	Abhishek Tripathi – Handled label offset calculations, assemble() function, and final compilation.

Acknowledgments

Special thanks to all contributors for their collaborative effort in building this RISC-V assembler.

Now **Registers, Helper Functions, and Contributions** are properly formatted and structured. Let me know if you need further modifications! 🚀
