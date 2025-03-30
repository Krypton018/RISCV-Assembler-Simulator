import os
import sys


registers = {
    "PC": 0,
    "00000": 0, "00001": 0, "00010": 380, "00011": 0, "00100": 0, "00101": 0,
    "00110": 0, "00111": 0, "01000": 0, "01001": 0, "01010": 0, "01011": 0,
    "01100": 0, "01101": 0, "01110": 0, "01111": 0, "10000": 0, "10001": 0,
    "10010": 0, "10011": 0, "10100": 0, "10101": 0, "10110": 0, "10111": 0,
    "11000": 0, "11001": 0, "11010": 0, "11011": 0, "11100": 0, "11101": 0,
    "11110": 0, "11111": 0
}


memory = {
    "10000": 0, "10004": 0, "10008": 0, "1000C": 0,
    "10010": 0, "10014": 0, "10018": 0, "1001C": 0,
    "10020": 0, "10024": 0, "10028": 0, "1002C": 0,
    "10030": 0, "10034": 0, "10038": 0, "1003C": 0,
    "10040": 0, "10044": 0, "10048": 0, "1004C": 0,
    "10050": 0, "10054": 0, "10058": 0, "1005C": 0,
    "10060": 0, "10064": 0, "10068": 0, "1006C": 0,
    "10070": 0, "10074": 0, "10078": 0, "1007C": 0,
}




def dec_to_bin(n):
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



def bin_to_dec(s):
    s = s.strip()
    n = len(s)
    num=0
    for i in range(n-1,-1,-1):
        num+=int(s[i])*(1<<(n-1-i))

    if s[0] == '1':  
        num = -((1 << n) - num)
    
    return num



def rSim(instruction):
    rs1=instruction[12:17]
    rs2=instruction[7:12]
    rd=instruction[20:25]

    if (rs1 not in registers or rs2 not in registers or rd not in registers):
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nInvalid Register \n')

    if(instruction[17:20]=="000" and instruction[0:7]=="0000000"):
        registers[rd]=registers[rs1]+registers[rs2]

    elif(instruction[17:20]=="000" and instruction[0:7]=="0100000"):
        registers[rd]=registers[rs1]-registers[rs2]

    elif(instruction[17:20]=="010" and instruction[0:7]=="0000000"):
        if(registers[rs1]<registers[rs2]):
            registers[rd]=1
        else:
            registers[rd]=0

    elif(instruction[17:20]=="101" and instruction[0:7]=="0000000"):
        rightshift=registers[rs2]&31
        registers[rd]=registers[rs1]>>rightshift

    elif(instruction[17:20]=="110" and instruction[0:7]=="0000000"):
        registers[rd]=registers[rs1]|registers[rs2]

    elif(instruction[17:20]=="111" and instruction[0:7]=="0000000"):
        registers[rd]=registers[rs1]&registers[rs2]
    
    else:
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nInvalid Instruction\n')
    return registers["PC"]+4



def lw(imm,rs1,rd):

    mem_add = bin_to_hex(sign_extend((dec_to_bin(registers[rs1]+bin_to_dec(imm))),20))
    if ((registers[rs1]+bin_to_dec(imm))%4 != 0):
        sys.exit(f"\nError on Line {registers['PC']//4 + 1}\nMemory address is not a multiple of 4\n")
    if (mem_add not in memory.keys()):
        sys.exit(f"\nError on Line {registers['PC']//4 + 1}\nAccessing Memory Location out of range\n")

    registers[rd]=memory[mem_add]
    return registers['PC'] + 4

def addi(imm,rs1,rd):
    registers[rd]=registers[rs1]+bin_to_dec(imm)
    return registers['PC'] + 4

def jalr(imm,rs1,rd):
    if (rd != "00000"):
        registers[rd]=registers["PC"]+4
    
    return_address = registers[rs1]+bin_to_dec(imm)
    if ((return_address)%4 != 0):
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nJump location is not a multiple of 4\n')
    return_address |= 1
    return_address ^= 1
    return return_address

def iSim(instruction):
    imm=instruction[:12]
    rs1=instruction[12:17]
    f3=instruction[17:20]
    rd=instruction[20:25]
    op=instruction[25:]


    if (rs1 not in registers or rd not in registers):
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nInvalid Register\n')

    if(op=="0000011" and f3=="010"):
        return_address = lw(imm,rs1,rd)
    elif (op=="0010011" and f3=="000"):
        return_address = addi(imm,rs1,rd)
    elif (op=="1100111" and f3=="000"):
        return_address = jalr(imm,rs1,rd)
    else:
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nInvalid Instruction\n')
    return return_address



def sSim(instruction):
    imm=instruction[0:7]+instruction[20:25]
    rs1=instruction[12:17]
    rs2=instruction[7:12]

    if (rs1 not in registers or rs2 not in registers):
        sys.exit(f"\nError on Line {registers['PC']//4 + 1}\nInvalid Register\n")

    mem_add = bin_to_hex(sign_extend((dec_to_bin(registers[rs1]+bin_to_dec(imm))),20))
    if ((registers[rs1]+bin_to_dec(imm))%4 != 0):
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nMemory address is not a multiple of 4\n')
    if (mem_add not in memory):
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nAccessing Memory Location out of range\n')

    memory[mem_add]=registers[rs2]
    return registers["PC"]+4



def bSim(instruction):
    immediate = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    immediate = bin_to_dec(immediate)

    vHalt = False
    
    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    

    if (rs1 not in registers or rs2 not in registers):
        sys.exit(f"\nError on line {(registers["PC"]//4) + 1}\nInvalid Register\n")


    if (funct3 == "000"):
        if (registers[rs1] == registers[rs2]):
            registers["PC"] += int(immediate)
            if (int(immediate) == 0 ):
                vHalt = True
        else:
            registers["PC"] += 4

    elif (funct3 == "001"):
        if (registers[rs1] != registers[rs2]):
            registers["PC"] += int(immediate)
            if (int(immediate) == 0 ):
                vHalt = True
        else:
            registers["PC"] += 4

    elif (funct3 == "100"):                        # BONUS blt INSTRUCTION
        if (registers[rs1] < registers[rs2]):
            registers["PC"] += int(immediate)
            if (int(immediate) == 0 ):
                vHalt = True
        else:
            registers["PC"] += 4

    else:
        sys.exit(f"\nError on Line {registers['PC']//4 + 1}\nInvalid Instruction\n")

    return registers["PC"], vHalt



def jSim(instruction):
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'
    rd = instruction[20:25]
    
    if (rd not in registers):
        sys.exit(f"\nError on Line {registers['PC']//4 + 1}\nInvalid Register\n")

    if (rd != "00000"):
        registers[rd] = registers['PC'] + 4

    if (bin_to_dec(imm)%4 == 0):
        return registers['PC'] + bin_to_dec(imm) 
    else:
        sys.exit(f'\nError on Line {registers['PC']//4 + 1}\nMemory address is not a multiple of 4\n')




# SIMULATE
def simulate(content):
    data = []
    halt = False

    instructions_list = [i.strip() for i in content]

    while(not halt):
        updated_registers = ""

        # All instructions have been read
        if(registers['PC']//4 >= len(instructions_list)):
            halt = True
            break

        instruction =  instructions_list[registers['PC']//4]
        
        opcode = instruction[-7:]
        
        if (opcode == '0110011'):
            registers['PC'] = rSim(instruction)

        elif (opcode == '0000011' or opcode == '0010011' or opcode == '1100111'):
            registers['PC'] = iSim(instruction)

        elif (opcode == '0100011'):
            registers['PC'] = sSim(instruction)
        
        elif (opcode == '1100011'):
            registers['PC'], halt = bSim(instruction)
        
        elif (opcode == '1101111'):
            registers['PC'] = jSim(instruction)

        else:
            sys.exit(f'\nInvalid Opcode on Line {registers['PC']//4 + 1}\n')
        
        # Hard Wiring x0 to 0
        registers['00000'] = 0
        
        for i in registers:
            temp = f"{registers[i] if int(registers[i]) >= 0 else (2**32+registers[i])} "
            updated_registers = updated_registers + temp 
        updated_registers = updated_registers + "\n"

        data.append(updated_registers)
        # print(updated_registers)

    
    for (address,value) in memory.items():
        memory_address = '000'+address
        memory_data = f"0x{memory_address}:{value}\n"

        data.append(memory_data)

    return data




# input_folder = "../automatedTesting/tests/bin/simple/simple_1.txt"
# output_folder = "../automatedTesting/tests/user_traces/simple/simple_1.txt"
# python3 Simulator.py ../automatedTesting/tests/bin/simple/simple_6.txt ../automatedTesting/tests/user_traces/simple/simple_6.txt
# pwd = (SimpleSimulator)

# python3 Simulator.py ..\automatedTesting\tests\bin\simple\simple_6.txt ..\automatedTesting\tests\user_traces\simple\simple_6.txt


input_file = sys.argv[1]
output_file = sys.argv[2]

if not os.path.isfile(input_file):
    sys.exit("\nInvalid File Path\n")

with open(input_file, 'r') as f:
    content = f.readlines()
    data = simulate(content)
with open(output_file, 'w') as f:
    f.writelines(data)




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