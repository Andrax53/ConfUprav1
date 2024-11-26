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
        # Process element at memory[100]
        ("read_memory", 2, 0, 100),
        ("bswap", 2, 2),
        ("write_memory", 0, 100, 2),

        # Process element at memory[101]
        ("read_memory", 2, 0, 101),
        ("bswap", 2, 2),
        ("write_memory", 0, 101, 2),

        # Process element at memory[102]
        ("read_memory", 2, 0, 102),
        ("bswap", 2, 2),
        ("write_memory", 0, 102, 2),

        # Process element at memory[103]
        ("read_memory", 2, 0, 103),
        ("bswap", 2, 2),
        ("write_memory", 0, 103, 2),

        # Process element at memory[104]
        ("read_memory", 2, 0, 104),
        ("bswap", 2, 2),
        ("write_memory", 0, 104, 2),
    ]

    binary = assembler(program)

    memory = [0] * 1024
    for i in range(5):
        memory[100 + i] = 0x12345678

    result = interpreter(memory, binary, 100, 5)

    expected = {
        "memory_values": {
            100: "0x12345678",
            101: "0x12345678",
            102: "0x12345678",
            103: "0x12345678",
            104: "0x12345678"
        }
    }
    assert result == expected
