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