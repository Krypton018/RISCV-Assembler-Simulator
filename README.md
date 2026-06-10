# RISC-V Assembler and Simulator

A custom-built, instruction-level Assembler and Simulator for the RISC-V instruction set architecture (ISA), written entirely in Python. 

This project provides a complete pipeline to translate human-readable RISC-V assembly code into 32-bit binary machine code, and subsequently simulate the execution of those instructions while accurately modeling hardware state, register updates, and memory access.

## Features

### 1. Assembler (`Assembler.py`)
* **Two-Pass Assembly:** Efficiently parses and translates assembly instructions into standard 32-bit binary representation.
* **Custom Bit-Manipulation Engine:** Handles precise immediate encoding, sign extensions, and opcode mapping without relying on external architecture libraries.
* **Comprehensive Format Support:** Accurately encodes instructions across multiple base RISC-V formats:
  * **R-type:** Register-to-register operations (e.g., `add`, `sub`, `and`).
  * **I-type:** Immediate operations and loads (e.g., `addi`, `lw`).
  * **S-type:** Store operations (e.g., `sw`).
  * **B-type:** Branching operations with target offset calculation (e.g., `beq`, `bne`).
  * **J-type:** Jump instructions with return address linking (e.g., `jal`).

### 2. Simulator (`Simulator.py`)
* **Instruction-Level Execution:** Reads the generated binary machine code and executes it instruction by instruction.
* **State Modeling:** Maintains a precise internal state of the 32 integer registers (`x0` to `x31`), ensuring `x0` remains hardwired to zero.
* **Memory Management:** Accurately simulates byte-addressable memory for `load` and `store` operations.
* **Control Flow:** Handles branching and jumping logic seamlessly, accurately updating the Program Counter (PC).

## Project Structure

```text
├── Assembler.py      # Core assembler logic and binary generation
├── Simulator.py      # Instruction execution and hardware state modeling
└── README.md         # Project documentation
