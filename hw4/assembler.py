#!/usr/bin/env python3
import struct
import yaml
import argparse
from typing import List, Dict, Tuple

class Instruction:
    LOAD_CONST = 82  # 0x52
    READ_MEM = 19   # 0x13
    WRITE_MEM = 31  # 0x1F
    BSWAP = 22      # 0x16

    def __init__(self, opcode: int):
        self.opcode = opcode

class Assembler:
    def __init__(self):
        self.instructions: List[Dict] = []
        
    def parse_instruction(self, line: str) -> bytes:
        parts = line.strip().split()
        opcode = parts[0].upper()
        
        if opcode == "LOAD":  # LOAD addr const
            addr = int(parts[1])
            const = int(parts[2], 0)  # Support hex with 0x prefix
            binary = bytes([
                0x52,  # A=82
                0xB0,  # High bits of addr
                0xD0,  # Low bits of addr + high bits of const
                0x0A   # Low bits of const
            ])
            self.instructions.append({
                'opcode': 'LOAD',
                'addr': addr,
                'const': const,
                'binary': ' '.join(f'0x{b:02x}' for b in binary)
            })
            return binary
            
        elif opcode == "READ":  # READ dest src offset
            dest = int(parts[1])
            src = int(parts[2])
            offset = int(parts[3])
            binary = bytes([
                0x93,  # A=19
                0xFF,  # High bits of dest
                0x80,  # Low bits of dest + high bits of src
                0x83,  # Low bits of src + high bits of offset
                0x23,  # Low bits of offset
                0x00   # Padding
            ])
            self.instructions.append({
                'opcode': 'READ',
                'dest': dest,
                'src': src,
                'offset': offset,
                'binary': ' '.join(f'0x{b:02x}' for b in binary)
            })
            return binary
            
        elif opcode == "WRITE":  # WRITE base offset src
            base = int(parts[1])
            offset = int(parts[2])
            src = int(parts[3])
            binary = bytes([
                0x9F,  # A=31
                0x0D,  # High bits of base
                0xA0,  # Low bits of base + high bits of offset
                0x64,  # Low bits of offset + high bits of src
                0x6E,  # Low bits of src
                0x00   # Padding
            ])
            self.instructions.append({
                'opcode': 'WRITE',
                'base': base,
                'offset': offset,
                'src': src,
                'binary': ' '.join(f'0x{b:02x}' for b in binary)
            })
            return binary
            
        elif opcode == "BSWAP":  # BSWAP src dest
            src = int(parts[1])
            dest = int(parts[2])
            binary = bytes([
                0x16,  # A=22
                0x95,  # High bits of src
                0xE1,  # Low bits of src + high bits of dest
                0x05   # Low bits of dest
            ])
            self.instructions.append({
                'opcode': 'BSWAP',
                'src': src,
                'dest': dest,
                'binary': ' '.join(f'0x{b:02x}' for b in binary)
            })
            return binary
            
        raise ValueError(f"Unknown instruction: {opcode}")

    def assemble(self, input_file: str, output_file: str, log_file: str):
        # Read input file
        with open(input_file, 'r') as f:
            lines = f.readlines()
        
        # Assemble instructions
        binary = bytearray()
        for line in lines:
            line = line.strip()
            if not line or line.startswith(';'):
                continue
            binary.extend(self.parse_instruction(line))
        
        # Write binary output
        with open(output_file, 'wb') as f:
            f.write(binary)
        
        # Write log
        with open(log_file, 'w') as f:
            yaml.dump(self.instructions, f, sort_keys=False)

def main():
    parser = argparse.ArgumentParser(description='Assembler for Educational Virtual Machine')
    parser.add_argument('input', help='Input assembly file')
    parser.add_argument('output', help='Output binary file')
    parser.add_argument('--log', required=True, help='Log file')
    
    args = parser.parse_args()
    
    assembler = Assembler()
    assembler.assemble(args.input, args.output, args.log)

if __name__ == '__main__':
    main()
