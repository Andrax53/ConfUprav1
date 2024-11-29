import pytest
from uvm import assembler, interpreter

def test_load_const():
    # Test loading constant 100 into register 0
    result = assembler([("load_const", 0, 100)])
    assert result == bytearray([0x52, 0x00, 0x64, 0x00, 0x00, 0x00])  # 32-bit format: opcode, reg, 4 bytes for value

def test_read_memory():
    # Test reading from memory using register 2 as target, register 0 as base, offset 0
    result = assembler([("read_memory", 2, 0, 0)])
    assert result == bytearray([0x13, 0x02, 0x00, 0x00, 0x00, 0x00])

def test_write_memory():
    # Test writing to memory using register 0 as base, offset 0, register 2 as source
    result = assembler([("write_memory", 0, 0, 2)])
    assert result == bytearray([0x1F, 0x00, 0x00, 0x02, 0x00, 0x00])

def test_bswap():
    # Test bswap using register 2 as both source and target
    result = assembler([("bswap", 2, 2)])
    assert result == bytearray([0x16, 0x02, 0x02, 0x00])

def test_program():
    # Test program to perform bswap on a vector of length 5
    program = [
        # Initialize vector with test values
        # First element
        ("load_const", 1, 0x12345678),
        ("write_memory", 0, 100, 1),
        
        # Second element
        ("load_const", 1, 0xAABBCCDD),
        ("write_memory", 0, 101, 1),
        
        # Third element
        ("load_const", 1, 0x87654321),
        ("write_memory", 0, 102, 1),
        
        # Fourth element
        ("load_const", 1, 0xFEDCBA98),
        ("write_memory", 0, 103, 1),
        
        # Fifth element
        ("load_const", 1, 0x11223344),
        ("write_memory", 0, 104, 1),
        
        # Set up base address in register 0
        ("load_const", 0, 100),
        
        # Process element at memory[100]
        ("read_memory", 2, 0, 0),
        ("bswap", 2, 2),
        ("write_memory", 0, 0, 2),

        # Process element at memory[101]
        ("read_memory", 2, 0, 1),
        ("bswap", 2, 2),
        ("write_memory", 0, 1, 2),

        # Process element at memory[102]
        ("read_memory", 2, 0, 2),
        ("bswap", 2, 2),
        ("write_memory", 0, 2, 2),

        # Process element at memory[103]
        ("read_memory", 2, 0, 3),
        ("bswap", 2, 2),
        ("write_memory", 0, 3, 2),

        # Process element at memory[104]
        ("read_memory", 2, 0, 4),
        ("bswap", 2, 2),
        ("write_memory", 0, 4, 2),
    ]

    binary = assembler(program)
    memory = [0] * 1024
    result = interpreter(memory, binary, 100, 5)

    # After bswap, each value should be byte-swapped
    expected = {
        "memory_values": {
            100: "0x78563412",  # bswap(0x12345678)
            101: "0xDDCCBBAA",  # bswap(0xAABBCCDD)
            102: "0x21436587",  # bswap(0x87654321)
            103: "0x98BADCFE",  # bswap(0xFEDCBA98)
            104: "0x44332211"   # bswap(0x11223344)
        }
    }
    assert result == expected

def test_single_bswap():
    # Test a single bswap operation
    program = [
        # Initialize first element
        ("load_const", 1, 0x12345678),
        ("write_memory", 0, 100, 1),
        
        # Set up base address
        ("load_const", 0, 100),
        
        # Perform bswap
        ("read_memory", 2, 0, 0),
        ("bswap", 2, 2),
        ("write_memory", 0, 0, 2),
    ]

    binary = assembler(program)
    memory = [0] * 1024
    result = interpreter(memory, binary, 100, 1)
    
    expected = {
        "memory_values": {
            100: "0x78563412"  # bswap(0x12345678)
        }
    }
    assert result == expected
