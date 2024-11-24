#!/usr/bin/env python3
import struct
import yaml
import argparse
from typing import List, Dict

class VirtualMachine:
    def __init__(self, memory_size: int = 4096):
        self.memory = bytearray(memory_size)
        
    def load_const(self, addr: int, const: int):
        """Load constant value into memory at specified address"""
        self.memory[addr] = const & 0xFF
        
    def read_mem(self, dest: int, src: int, offset: int):
        """Read value from memory with offset and store at destination"""
        addr = (self.memory[src] + offset) & 0xFF
        self.memory[dest] = self.memory[addr]
        
    def write_mem(self, base: int, offset: int, src: int):
        """Write value from source to memory location with offset"""
        addr = (self.memory[base] + offset) & 0xFF
        self.memory[addr] = self.memory[src]
        
    def bswap(self, src: int, dest: int):
        """Perform byte swap operation"""
        value = self.memory[src]
        # For single byte values, we just reverse the bits
        swapped = int(format(value, '08b')[::-1], 2)
        self.memory[dest] = swapped

    def execute_instruction(self, binary: bytes) -> None:
        if len(binary) == 4:  # 4-byte instruction
            instruction = struct.unpack('>I', binary)[0]
            opcode = instruction >> 25
            
            if opcode == 82:  # LOAD_CONST
                addr = (instruction >> 13) & 0xFFF
                const = instruction & 0x3FF
                self.load_const(addr, const)
            elif opcode == 22:  # BSWAP
                src = (instruction >> 13) & 0xFFF
                dest = instruction & 0xFFF
                self.bswap(src, dest)
                
        elif len(binary) == 6:  # 6-byte instruction
            instruction = int.from_bytes(binary, 'big')
            opcode = instruction >> 35
            
            if opcode == 19:  # READ_MEM
                dest = (instruction >> 23) & 0xFFF
                src = (instruction >> 11) & 0xFFF
                offset = instruction & 0x7FF
                self.read_mem(dest, src, offset)
            elif opcode == 31:  # WRITE_MEM
                base = (instruction >> 23) & 0xFFF
                offset = (instruction >> 13) & 0x3FF
                src = instruction & 0xFFF
                self.write_mem(base, offset, src)

    def execute(self, binary_file: str, result_file: str, start_addr: int, end_addr: int):
        # Read binary file
        with open(binary_file, 'rb') as f:
            program = f.read()
            
        # Execute program
        pos = 0
        while pos < len(program):
            if pos + 6 <= len(program) and (program[pos] >> 1) in [19, 31]:
                self.execute_instruction(program[pos:pos+6])
                pos += 6
            else:
                self.execute_instruction(program[pos:pos+4])
                pos += 4
                
        # Save results
        results = {
            'memory_range': {
                'start': start_addr,
                'end': end_addr,
                'values': [self.memory[i] for i in range(start_addr, end_addr + 1)]
            }
        }
        
        with open(result_file, 'w') as f:
            yaml.dump(results, f)

def main():
    parser = argparse.ArgumentParser(description='Interpreter for Educational Virtual Machine')
    parser.add_argument('binary', help='Input binary file')
    parser.add_argument('output', help='Output YAML file')
    parser.add_argument('--start', type=int, required=True, help='Start address of memory range')
    parser.add_argument('--end', type=int, required=True, help='End address of memory range')
    
    args = parser.parse_args()
    
    vm = VirtualMachine()
    vm.execute(args.binary, args.output, args.start, args.end)

if __name__ == '__main__':
    main()
