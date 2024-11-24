#!/usr/bin/env python3
import os
import pytest
from assembler import Assembler
from interpreter import VirtualMachine

def test_load_const():
    # Test case from specification
    binary = bytes([0x52, 0xB0, 0xD0, 0x0A])
    vm = VirtualMachine()
    vm.execute_instruction(binary)
    assert vm.memory[352] == 346 & 0xFF

def test_read_mem():
    # Test case from specification
    binary = bytes([0x93, 0xFF, 0x80, 0x83, 0x23, 0x00])
    vm = VirtualMachine()
    vm.execute_instruction(binary)
    # Set up test data
    vm.memory[112] = 10  # Source address
    vm.memory[10 + 71] = 42  # Value at source + offset
    assert vm.memory[511] == 42

def test_write_mem():
    # Test case from specification
    binary = bytes([0x9F, 0x0D, 0xA0, 0x64, 0x6E, 0x00])
    vm = VirtualMachine()
    vm.execute_instruction(binary)
    # Set up test data
    vm.memory[27] = 50  # Base address
    vm.memory[883] = 42  # Source value
    assert vm.memory[50 + 148] == 42

def test_bswap():
    # Test case from specification
    binary = bytes([0x16, 0x95, 0xE1, 0x05])
    vm = VirtualMachine()
    vm.memory[810] = 0x12345678 & 0xFF
    vm.execute_instruction(binary)
    assert vm.memory[188] == 0x78563412 & 0xFF

def test_full_program():
    # Create temporary files for testing
    asm_file = "test.asm"
    bin_file = "test.bin"
    log_file = "test.log"
    result_file = "test.result"
    
    # Write test program
    with open(asm_file, "w") as f:
        f.write("""
LOAD 100 0x12
LOAD 101 0x34
BSWAP 100 100
BSWAP 101 101
""")
    
    # Assemble program
    assembler = Assembler()
    assembler.assemble(asm_file, bin_file, log_file)
    
    # Execute program
    vm = VirtualMachine()
    vm.execute(bin_file, result_file, 100, 101)
    
    # Verify results
    assert vm.memory[100] == 0x48 & 0xFF  # 0x12 swapped
    assert vm.memory[101] == 0x2C & 0xFF  # 0x34 swapped
    
    # Clean up
    for file in [asm_file, bin_file, log_file, result_file]:
        if os.path.exists(file):
            os.remove(file)

if __name__ == '__main__':
    pytest.main([__file__])
