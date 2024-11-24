import pytest
from uvm import assembler, interpreter

def test_load_const():
    # Test (A=82, B=352, C=346)
    result = assembler([("load_const", 352, 346)])
    assert result == bytearray([0x52, 0xB0, 0xD0, 0x0A])

def test_read_memory():
    # Test (A=19, B=511, C=112, D=71)
    result = assembler([("read_memory", 511, 112, 71)])
    assert result == bytearray([0x93, 0xFF, 0x80, 0x83, 0x23, 0x00])

def test_write_memory():
    # Test (A=31, B=27, C=148, D=883)
    result = assembler([("write_memory", 27, 148, 883)])
    assert result == bytearray([0x9F, 0x0D, 0xA0, 0x64, 0x6E, 0x00])

def test_bswap():
    # Test (A=22, B=810, C=188)
    result = assembler([("bswap", 810, 188)])
    assert result == bytearray([0x16, 0x95, 0xE1, 0x05])

def test_program():
    # Test program to perform bswap on a vector of length 5
    program = [
        ("load_const", 0, 5),  # Load vector length
        ("load_const", 1, 0),  # Initialize counter
        "loop_start:",
        ("read_memory", 2, 1, 100),  # Read vector element (base addr 100)
        ("bswap", 2, 2),  # Perform bswap
        ("write_memory", 1, 0, 2),  # Write back result
        ("load_const", 2, 1),  # Load increment
        ("add", 1, 1, 2),  # Increment counter
        ("cmp", 1, 0),  # Compare counter with length
        ("jl", "loop_start"),  # Jump if less
    ]
    result = assembler(program)
    # Add assertions for the expected byte pattern
