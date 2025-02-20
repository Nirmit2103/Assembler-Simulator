import re

registers = {
    "x0": "00000",  # zero
    "x1": "00001",  # ra (return address)
    "x2": "00010",  # sp (stack pointer)
    "x3": "00011",  # gp (global pointer)
    "x4": "00100",  # tp (thread pointer)
    "x5": "00101",  # t0 (temporary)
    "x6": "00110",  # t1 (temporary)
    "x7": "00111",  # t2 (temporary)
    "x8": "01000",  # s0 / fp (saved / frame pointer)
    "x9": "01001",  # s1 (saved)
    "x10": "01010", # a0 (argument)
    "x11": "01011", # a1 (argument)
    "x12": "01100", # a2 (argument)
    "x13": "01101", # a3 (argument)
    "x14": "01110", # a4 (argument)
    "x15": "01111", # a5 (argument)
    "x16": "10000", # a6 (argument)
    "x17": "10001", # a7 (argument)
    "x18": "10010", # s2 (saved)
    "x19": "10011", # s3 (saved)
    "x20": "10100", # s4 (saved)
    "x21": "10101", # s5 (saved)
    "x22": "10110", # s6 (saved)
    "x23": "10111", # s7 (saved)
    "x24": "11000", # s8 (saved)
    "x25": "11001", # s9 (saved)
    "x26": "11010", # s10 (saved)
    "x27": "11011", # s11 (saved)
    "x28": "11100", # t3 (temporary)
    "x29": "11101", # t4 (temporary)
    "x30": "11110", # t5 (temporary)
    "x31": "11111",  # t6 (temporary)
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

def to_binary(value, bits):
    if value is None:
        return "0" * bits 
    if value < 0:
        value = (1 << bits) + value  
    return format(value, f'0{bits}b')[-bits:]

####################################################################
#RTYPE

R_op= "0110011"
R_f7 = {
    "add": "0000000",
    "sub": "0100000",
    "slt": "0000000",
    "srl": "0000000",
    "or": "0000000",
    "and": "0000000"
}

R_f3 = {
    "add": "000",
    "sub": "000",
    "slt": "010",
    "srl": "101",
    "or": "110",
    "and": "111"
}


def rbin(f7, rd, rs1, rs2):
    return R_f7[f7] + registers[rs2] + registers[rs1] + R_f3[f7] + registers[rd] + R_op


####################################################################
#ITYPE

I_f3 = {
    "lw": "010",
    "addi": "000",
    "jalr": "000"
}

I_op = {
    "lw": "0000011",
    "addi": "0010011",
    "jalr": "1100111"
}


def ibin(instr,rd,rs1,imm):
    if instr == "lw":
        return to_binary(int(rs1), 12) + registers[imm] + I_f3[instr] + registers[rd] + I_op[instr]
    else:
        return to_binary(int(imm), 12) + registers[rs1] + I_f3[instr] + registers[rd] + I_op[instr]


#####################################################################
#STYPE




S_f3 = {
    "sw": "010"
}

S_op = {
    "sw": "0100011"
}


def sbin(instr, rs2, imm, rs1):
    imm_bin = to_binary(int(imm), 12)
    return imm_bin[:7] + registers[rs2] + registers[rs1] + S_f3[instr] + imm_bin[7:] + S_op[instr]

######################################################################
#BTYPE



B_f3 = {
    "beq": "000",
    "bne": "001",
    "blt": "100",
    "bge": "101",
    "bltu": "110",
    "bgeu": "111"
}

B_op = "1100011"



def bbin(instr, rs1, rs2, imm):
    imm_bin = to_binary(int(imm), 13)  
    return imm_bin[0] + imm_bin[2:8] + registers[rs2] + registers[rs1] + B_f3[instr] + imm_bin[8:12] + imm_bin[1] + B_op


########################################################################
#JTYPE
J_op = "1101111"


def jbin(rd, imm):
    imm_bin = to_binary(int(imm), 21)  
    return imm_bin[0] + imm_bin[10:20] + imm_bin[9] + imm_bin[1:9] + registers[rd] + J_op



#########################################################################

def take_input(filename):
    with open(filename, "r") as f:
        commands = f.readlines()
    commands = [line.strip() for line in commands if line.strip()]
    processed_commands = []
    for line in commands:
        tokens = re.split(r'[ ,]', line)
        processed_line = []
        for token in tokens:
            if '(' in token and ')' in token:
                # Fix: Separate imm and rs1 properly
                imm = token[:token.index('(')]
                rs1 = token[token.index('(') + 1 : token.index(')')]
                processed_line.extend([imm, rs1])
            else:
                processed_line.append(token)
        processed_commands.append(processed_line)
    return processed_commands


#######################################################################

def typeof(command):
    instr = command[0].strip()  # Remove any extra spaces

    if instr in R_f3:
        return "R"
    if instr in I_f3:
        return "I"
    if instr in S_f3:
        return "S"
    if instr in B_f3:  
        return "B"
    if instr == "jal":  
        return "J"
    if instr == "jalr":
        return "I"
    if instr == "lw":
        return "I"
    if instr == "addi":
        return "I"
    if instr == "sw":
        return "S"

######################################################################

# def calculate_offset_for_labels(commands):
#     new_commands = []
#     label_positions = {}
#     for i in range(len(commands)):
#         if commands[i][0].endswith(":"):  
#             label_positions[commands[i][0][:-1]] = i  
#     for i in range(len(commands)):
#         if commands[i][0].endswith(":"):  
#             continue  
#         if commands[i][-1] not in registers:
#             if commands[i][-1].lstrip('-').isdigit():
#                 new_commands.append(commands[i])
#             else:
#                 label_name = commands[i][-1]
#                 if label_name in label_positions:
#                     j = label_positions[label_name]
#                     if typeof(commands[i][0]) == "B":
#                         offset = (j - i)*2
#                     elif typeof(commands[i][0]) == "J":
#                         offset = (j - i) * 4
#                     new_commands.append(commands[i][:-1] + [offset])
#                 else:
#                     new_commands.append(commands[i])
#         else:
#             new_commands.append(commands[i])
#     return new_commands

def calculate_offset_for_labels(commands):
    new_commands = []
    label_positions = {}
    inst_index = 0

    
    for cmd in commands:
        
        if cmd[0].endswith(":") and len(cmd) > 1:
            label_positions[cmd[0][:-1]] = inst_index
            inst_index += 1
        elif cmd[0].endswith(":"):
            
            label_positions[cmd[0][:-1]] = inst_index
        else:
            inst_index += 1

    
    inst_index = 0
    for cmd in commands:
        
        if cmd[0].endswith(":"):
            if len(cmd) > 1:
                inst = cmd[1:]
            else:
                continue  
        else:
            inst = cmd

        if inst[-1] not in registers and not inst[-1].lstrip('-').isdigit():
            label_name = inst[-1]
            if label_name in label_positions:
                target = label_positions[label_name]
                instr_type = typeof(inst)
                print(inst)
                if instr_type in "B":
                    offset = (target - (inst_index))*4

                elif instr_type in "J":   
                    offset = (target - (inst_index))*4   

                    
                else:
                    offset = 0
                new_commands.append(inst[:-1] + [offset])
            else:
                print(f"Warning: Label '{label_name}' not found!")
                new_commands.append(inst)
        else:
            new_commands.append(inst)
        inst_index += 1
    return new_commands




def assemble(commands):
    binary=[]
    for cmd in commands:
        if typeof(cmd)== "R":
            binary.append(rbin(cmd[0], cmd[1], cmd[2], cmd[3]))
        elif typeof(cmd)== "I":
            binary.append(ibin(cmd[0], cmd[1], cmd[2], cmd[3]))
        elif typeof(cmd)== "S":
            binary.append(sbin(cmd[0], cmd[1], cmd[2], cmd[3]))
        elif typeof(cmd)== "B":
            binary.append(bbin(cmd[0], cmd[1], cmd[2], cmd[3]))
        elif typeof(cmd)== "J":
            binary.append(jbin(cmd[1], cmd[2]))
    return binary

filename = str(input("Enter filename: "))
commands = take_input(filename)
commands = calculate_offset_for_labels(commands)

binary=assemble(commands)
for line in binary:
    print(line)

#CONTRIBUTIONS:

    #ARJUN AND AYUSH - primary instruction type functions and type of function
    #NIRMIT JAIN - input function and binary helper function 
    #ABHISHEK TRIPATHI - offset calculations and assemble function, Final Compilation









