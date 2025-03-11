import os
import sys



registers = {
    "PC": 0,
    "00000": 0, "00001": 0, "00010": 0, "00011": 0, "00100": 0, "00101": 0,
    "00110": 0, "00111": 0, "01000": 0, "01001": 0, "01010": 0, "01011": 0,
    "01100": 0, "01101": 0, "01110": 0, "01111": 0, "10000": 0, "10001": 0,
    "10010": 0, "10011": 0, "10100": 0, "10101": 0, "10110": 0, "10111": 0,
    "11000": 0, "11001": 0, "11010": 0, "11011": 0, "11100": 0, "11101": 0,
    "11110": 0, "11111": 0
}


memory = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# dhruv
'''--------------------------------------------------------------------------------------'''
def bin_to_hex(bin_str):
    hex_dict = {10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
    

    if (len(bin_str)%4 != 0):
            bin_str = str(bin_str[0])*(4 - len(bin_str)%4) + bin_str


    hex_str = ""
    while (bin_str != ""):
        val = int(bin_str[0])*8 + int(bin_str[1])*4 + int(bin_str[2])*2 + int(bin_str[3])*1

        if (val in hex_dict):
            hex_str = hex_str + hex_dict[val]
        else:
            hex_str = hex_str + str(val) 

        bin_str = bin_str[4:]

    return hex_str



def bSim(instruction):
    immediate = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24]
    
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    

    if (rs1 not in registers or rs2 not in registers):
        print(f"Invalid Register on line {(registers["PC"]/4)+4}")


    if (funct3 == "000"):
        if (registers[rs1] == registers[rs2]):
            registers["PC"] += int(immediate)
        else:
            registers["PC"] += 4

    elif (funct3 == "001"):
        if (registers[rs1] != registers[rs2]):
            registers["PC"] += int(immediate)
        else:
            registers["PC"] += 4

    else:
        print("Invalid funct3 value")

    return registers["PC"]
'''---------------------------------------------------------------------------------------------'''
# Ashmit
'''----------------------------------------------------------------------------------------------'''
def bin_to_dec():pass
def rSim(instruction):
    rs1=instruction[12:17]
    rs2=instruction[7:12]
    rd=instruction[20:25]
    if(instruction[17:20]=="000" and instruction[0:7]=="0000000"):
        registers[rd]=registers[rs1]+registers[rs2]

    elif(instruction[17:20]=="000" and instruction[0:7]=="0100000"):
        registers[rd]=registers[rs1]-registers[rs2]

    elif(instruction[17:20]=="010"):
        if(registers[rs1]<registers[rs2]):
            registers[rd]=1
        else:
            registers[rd]=0

    elif(instruction[17:20]=="101"):
        rightshift=registers[rs2]&31
        registers[rd]=registers[rs1]>>rightshift

    elif(instruction[17:20]=="110"):
        registers[rd]=registers[rs1]|registers[rs2]

    elif(instruction[17:20]=="111"):
        registers[rd]=registers[rs1]&registers[rs2]
    
    return registers["PC"]+4

def sSim(instruction):
    imm=instruction[0:7]+instruction[20:25]
    rs1=instruction[12:17]
    rs2=instruction[7:12]
    memory[registers[rs1]+bin_to_dec(imm)]=rs2
    return registers["PC"]+4
'''------------------------------------------------------------------------------------------'''
#immediate value expression for J type (Dhruv's expression, not Bhavya's)-->
#immediate = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11]







# BASE CONVERSIONS
# bin to dec (2s complement)
# perform algebraic in decimal
# dec to bin (For writing in O/P)

# dec to hex (For writing in O/P) 


# INSTRUCTION SIMULATING
# r-sim
# i-sim
# s-sim
# b-sim     [UPDATE PC]
# j-sim     [UPDATE PC]


# SIMULATE
# Simulator will work according to the PC, it will execute instruction at index PC/4
# Initially retrieve opcode and simulate according to corresponding instruction type
# Update PC [Get updated PC value from instruction-sim]
# Go to next PC/4
# Check for Virtual Halt


# Print all register values after each instruction (All space separated registers in same line)
# Print memory location after all instructions have been executed (All memory locaations in different lines)


# FILE PARSE
# Initially check via printing, later use File I/O



# ERROR HANDLING