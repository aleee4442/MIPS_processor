# MIPS Processor Simulator

A complete MIPS architecture simulator implemented in Python that processes binary instructions and simulates processor execution. This project demonstrates deep understanding of computer architecture and low-level system operations.

## Features

- **Binary Instruction Processing**: Reads and executes MIPS instructions in binary format
- **Register Management**: 32 general-purpose registers with real-time state tracking
- **Program Counter Simulation**: Accurate PC management and instruction sequencing
- **Memory-Mapped Output**: Generates comprehensive dump files for analysis
- **Complete MIPS ISA Support**: Handles R-type, I-type, and J-type instructions

## Supported Instructions

### R-Type Instructions (OPCODE 000000)
- `ADD` (100000) - Add registers
- `SUB` (100010) - Subtract registers  
- `AND` (100100) - Bitwise AND
- `OR` (100101) - Bitwise OR
- `SLT` (101010) - Set less than

### I-Type Instructions
- `ADDI` (001000) - Add immediate
- `LW` (100011) - Load word
- `SW` (101011) - Store word
- `BEQ` (000100) - Branch if equal
- `BNE` (000101) - Branch if not equal

### J-Type Instructions
- `J` (000010) - Jump
- `JAL` (000011) - Jump and link

## Installation

```bash
git clone git@github.com:aleee4442/MIPS_processor.git
cd MIPS_processor
```

## Usage

### Running the Simulator
```bash
python sim.py
```
The simulator will:
1. Read binary instructions from `sample_program.txt`
2. Execute the MIPS program
3. Generate `instr_dump.txt` with instruction memory
4. Generate `memory_dump.txt` with register states

### Input Format
Create `sample_program.txt` with binary instructions (one per line):
```
00100000000010000000000000000101  # ADDI $t0, $zero, 5
00100000000010010000000000001010  # ADDI $t1, $zero, 10
00000001000010010101000000100000  # ADD $t2, $t0, $t1
```

### Output Files

**instr_dump.txt** - Instruction memory mapping:
```
0x0 00100000000010000000000000000101
0x1 00100000000010010000000000001010
0x2 00000001000010010101000000100000
```

**memory_dump.txt** - Register states after execution:
```
PC 00000000000000000000000000001100
t0 00000000000000000000000000000101
t1 00000000000000000000000000001010
t2 00000000000000000000000000001111
```

## Architecture Overview

### Modular Design
- **sim.py**: Main simulator and program entry point
- **CPU.py**: Central processing unit with instruction execution logic
- **RAM.py**: Memory management and storage system
- **regs.py**: Register file implementation and management
- **utils.py**: Utility functions and helpers

### Execution Flow
1. **Instruction Fetch**: `sim.py` reads binary instructions into RAM
2. **Instruction Decode**: `CPU.py` parses 32-bit binary instructions
3. **Execute**: ALU operations performed based on instruction type
4. **Memory Access**: `RAM.py` handles load/store operations
5. **Write Back**: `regs.py` updates register file with results
6. **PC Management**: Handles instruction sequencing and control flow

## Project Structure

```
MIPS_processor/
├── sim.py                # Main simulator and program entry point
├── CPU.py                # Central Processing Unit implementation
├── RAM.py                # Memory management system
├── regs.py               # Register file implementation
├── utils.py              # Utility functions and helpers
├── sample_program.txt    # Example binary program
├── instr_dump.txt        # Generated instruction memory
├── memory_dump.txt       # Generated register states
├── registers_dump.txt    # Detailed register contents
└── README.md             # This file
```
## Module Responsibilities
- **CPU.py**: Instruction decoding, ALU operations, control logic
- **RAM.py**: Memory read/write operations, address management
- **regs.py**: Register read/write, register file management
- **utils.py**: Binary conversions, file I/O, helper functions
- **sim.py**: Orchestrates execution flow and module coordination

## Learning Outcomes

This project provided hands-on experience with:
- Computer architecture and processor design
- Modular software design for complex systems
- Binary instruction decoding and execution
- Register file management and data pathways
- Memory hierarchy and address management
- Low-level binary operations and bit manipulation
