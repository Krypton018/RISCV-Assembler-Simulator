import os
import re
registers = {"zero":"00000", 
             "ra":"00001", 
             "sp":"00010", 
             "gp":"00011", 
             "tp":"00100", 
             "t0":"00101",
             "t1":"00110", "t2":"00111",  
             "s0":"01000", "fp":"01000", 
             "s1":"01001", 
             "a0":"01010", "a1":"01011", 
             "a2":"01100", "a3":"01101", "a4":"01110", "a5":"01111", "a6":"10000", "a7":"10001",
             "s2":"10010", "s3":"10011", "s4":"10100", "s5":"10101", "s6":"10110", "s7":"10111", "s8":"11000", "s9":"11001", "s10":"11010", "s11":"11011", 
             "t3":"11100", "t4":"11101", "t5":"11110", "t6":"11111"
}    

R_TYPE = {"add" : {"opcode":"0110011", "funct3":"000", "funct7":"0000000"}, 
          "sub" : {"opcode":"0110011", "funct3":"000", "funct7":"0100000"}, 
          "slt" : {"opcode":"0110011", "funct3":"010", "funct7":"0000000"}, 
          "srl" : {"opcode":"0110011", "funct3":"101", "funct7":"0000000"},
          "or"  : {"opcode":"0110011", "funct3":"110", "funct7":"0000000"},
          "and" : {"opcode":"0110011", "funct3":"111", "funct7":"0000000"}}

I_TYPE = {"lw"   : {"opcode":"0000011", "funct3":"010"},
          "addi" : {"opcode":"0010011", "funct3":"000"},
          "jalr" : {"opcode":"1100111", "funct3":"000"}}

S_TYPE = {"sw" : {"opcode":"0100011", "funct3":"010"}}

B_TYPE = {"beq" : {"opcode":"1100011", "funct3":"000"},
          "bne" : {"opcode":"1100011", "funct3":"001"},
          "blt" : {"opcode":"1100011", "funct3":"000"}}

J_TYPE = {"jal" : {"opcode":"1101111"}}

def sign_extend(binary, n):
    bit = binary[0]
    return ((n-len(binary))*bit) + binary

def r_parse(operation, arguements):
    rd, rs1, rs2 = re.split(',', arguements)
    inst = R_TYPE[operation]["funct7"] +  registers[rs2] +  registers[rs1] +  R_TYPE[operation]["funct3"] +  registers[rd] +  R_TYPE[operation]["opcode"]
    return inst

def i_parse(oper,arg):
    pass
def s_parse(oper,arg):
    pass
def j_parse(oper,arg):
    pass
def b_parse(oper,arg):
    pass


def get_labels(content):
    labels = {}
    for line_number, line in enumerate(content):
        line = line.strip()
        if ":" in line:
            label = line.split(":")[0]
            labels[label] = line_number
    return labels


def assemble(content):
    labels = get_labels(content)
    data = ""
    for line_number, line in enumerate(content):
        line = line.strip()
        if ":" in line:
            instruction = line.split(":")[1]
        else:
            instruction=line
        instruction = instruction.strip()
        operation, arguments = instruction.split(" ")

        if operation in R_TYPE:
            data += r_parse(operation,arguments) + "\n"
        elif operation in I_TYPE:
            data += i_parse(operation,arguments) + "\n"
        elif operation in S_TYPE:
            data += s_parse(operation,arguments) + "\n"
        elif operation in J_TYPE:
            data += j_parse(operation,arguments,labels,line_number) + "\n"
        elif operation in B_TYPE:
            data += b_parse(operation,arguments,labels,line_number) + "\n"
    print(data.strip())

def parse(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                content = file.readlines()
                assemble(content)
                print(f"Contents of {filename}:\n{content}\n")


folder_path = r"..\automatedTesting\tests\assembly\simpleBin"

# \CO_Project_Allocated_jan30_2025\CO_Project_Allocated_jan30_2025

parse(folder_path)