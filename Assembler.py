import os
import re
import sys

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
             "t3":"11100", "t4":"11101", "t5":"11110", "t6":"11111"}    

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


def to_bin(n):
    binary = ""
    if n==0:
        return "0"
    
    neg = n<0
    if neg:
        n = -n
    
    while (n!=0):
        if n%2==0:
            binary = "0"+binary
        else:
            binary = "1"+binary
        n//=2   
    binary = "0"+binary 

    if (neg):
        flipped = ""
        piv = False
        for i in range(len(binary)-1, -1, -1):
            if not piv:
                if binary[i]=="0":
                    flipped = "0"+flipped
                else:
                    flipped = "1"+flipped
                    piv = True
            else:
                if binary[i]=="0":
                    flipped = "1"+flipped
                else:
                    flipped = "0"+flipped
        binary = flipped

    return binary   


def sign_extend(binary, n):
    bit = binary[0]
    return ((n-len(binary))*bit) + binary


def r_parse(operation, arguements, line_number):
    rd, rs1, rs2 = re.split(',', arguements)

    if ((rd not in registers) or (rs1 not in registers) or (rs2 not in registers)):
        sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid register name\n")
    
    inst = R_TYPE[operation]["funct7"] +  registers[rs2] +  registers[rs1] +  R_TYPE[operation]["funct3"] +  registers[rd] +  R_TYPE[operation]["opcode"]
    return inst


def i_parse(operation, arguements, line_number):
    if operation=='lw':
        arguements = arguements.rstrip(")")
        rd, imm, rs1 = re.split(r'[,(]', arguements)
        
        if((rd not in registers) or (rs1 not in registers)):
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid register name\n")
        elif(not(imm.strip("-").isdigit() and imm !="-")):
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid Immediate\n")
        
        imm = sign_extend(to_bin(int(imm)), 12)
        inst = imm + registers[rs1] + I_TYPE[operation]["funct3"] + registers[rd] + I_TYPE[operation]["opcode"]
    else:
        rd, rs1, imm = re.split(',', arguements)
        
        if((rd not in registers) or (rs1 not in registers)):
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid register name\n")
        elif(not(imm.strip("-").isdigit() and imm !="-")):
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid Immediate\n")
        
        imm = sign_extend(to_bin(int(imm)), 12)
        inst = imm + registers[rs1] + I_TYPE[operation]["funct3"] + registers[rd] + I_TYPE[operation]["opcode"]
    
    return inst


def s_parse(operation, arguments, line_number):
    arguments = arguments.rstrip(")")
    rs2, imm, rs1 = re.split(r'[,(]', arguments)

    if((rs2 not in registers) or (rs1 not in registers)):
        sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid register name\n")
    elif(not(imm.strip("-").isdigit() and imm !="-")):
        sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid Immediate\n")

    imm = sign_extend(to_bin(int(imm)), 12)
    inst = imm[:7] + registers[rs2] + registers[rs1] + S_TYPE[operation]["funct3"] + imm[7:] + S_TYPE[operation]["opcode"]
    
    return inst


def b_parse(operation, arguments, labels, line_number):
    rs1, rs2, imm = re.split(',', arguments)
    
    if((rs2 not in registers) or (rs1 not in registers)):
        sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid register name\n")
    
    if (not(imm.strip("-").isdigit() and imm !="-")):
        if imm in labels:
            imm = (labels[imm]-line_number)*4
        else:
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid Immediate\n")

    imm = sign_extend(to_bin(int(imm)), 13)
    inst = imm[0] + imm[2:8] + registers[rs2] + registers[rs1] + B_TYPE[operation]["funct3"] + imm[8:-1] + imm[1] + B_TYPE[operation]["opcode"]
    return inst


def j_parse(operation,arguments, labels, line_number):
    rd, imm = re.split(',', arguments)
    
    if (rd not in registers):
        sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid register name\n")
    
    if (not(imm.strip("-").isdigit() and imm !="-")):
        if imm in labels:
            imm = (labels[imm]-line_number)*4
        else:
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid Immediate\n")
        
    imm = sign_extend(to_bin(int(imm)), 21)
    inst = imm[0] + imm[10:-1] + imm[9] + imm[1:9] + registers[rd] + J_TYPE[operation]["opcode"]
    return inst


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
    data = []
    for line_number, line in enumerate(content):
        if (line=="\n"):
            continue
        line = line.strip()
        if ":" in line:
            instruction = line.split(":")[1]
        else:
            instruction=line
        instruction = instruction.strip()
        operation, arguments = instruction.split(" ")

        if operation in R_TYPE:
            curr = r_parse(operation,arguments,line_number)
            data.append(curr + "\n")
        elif operation in I_TYPE:
            curr = i_parse(operation,arguments,line_number)
            data.append(curr + "\n")
        elif operation in S_TYPE:
            curr = s_parse(operation,arguments,line_number)
            data.append(curr + "\n")
        elif operation in J_TYPE:
            curr = j_parse(operation,arguments,labels,line_number)
            data.append(curr + "\n")
        elif operation in B_TYPE:
            curr = b_parse(operation,arguments,labels,line_number)
            data.append(curr + "\n")         
        else:
            sys.exit(f"\nInvalid Instruction on Line {line_number}\nInvalid Instruction type\n")

    return data


# input_folder = r"..\automatedTesting\tests\assembly\simpleBin\Ex_test_0.txt"
# output_folder = r"..\automatedTesting\tests\assembly\user_bin_s\Ex_test_0.txt"

input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isfile(input_file):
    sys.exit("Invalid File Path")


with open(input_file, 'r') as f:
    content = f.readlines()
    data = assemble(content)
if data!=None:
    with open(output_file, 'w') as f:
        f.writelines(data)