import pytest
from uvm import assembler, interpreter

def test_load_const():
    # Test loading constant 100 into register 0
    result = assembler([("load_const", 0, 100)])
    assert result == bytearray([0x52, 0x00, 0x64, 0x00])

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
        # Set up base address
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

    # Initialize memory with test values
    memory = [0] * 1024
    for i in range(5):
        memory[100 + i] = 0x12345678

    result = interpreter(memory, binary, 100, 5)

    # After bswap, each value should be byte-swapped
    expected = {
        "memory_values": {
            100: "0x78563412",
            101: "0x78563412",
            102: "0x78563412",
            103: "0x78563412",
            104: "0x78563412"
        }
    }
    assert result == expected

def test_single_bswap():
    # Test a single bswap operation
    program = [
        ("load_const", 0, 100),
        ("read_memory", 2, 0, 0),
        ("bswap", 2, 2),
        ("write_memory", 0, 0, 2),
    ]

    binary = assembler(program)
    memory = [0] * 1024
    memory[100] = 0x12345678

    result = interpreter(memory, binary, 100, 1)
    expected = {
        "memory_values": {
            100: "0x78563412"
        }
    }
    assert result == expected
