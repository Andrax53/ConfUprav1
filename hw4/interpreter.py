import sys
import yaml
import struct

def interpret(input_file, output_file, memory_range):
    with open(input_file, 'rb') as f:
        binary_data = f.read()

    memory = [0] * 1024  # Предположим, что память УВМ имеет размер 1024 байта
    pc = 0

    while pc < len(binary_data):
        A = binary_data[pc]
        if A == 82:  # LOAD_CONST
            B = binary_data[pc + 1]
            C = struct.unpack('>I', binary_data[pc + 2:pc + 6])[0]
            memory[B] = C
            pc += 6
        elif A == 19:  # READ_MEM
            B = binary_data[pc + 1]
            C = struct.unpack('>I', binary_data[pc + 2:pc + 6])[0]
            D = struct.unpack('>H', binary_data[pc + 6:pc + 8])[0]
            address = memory[C] + D
            memory[B] = memory[address]
            pc += 8
        elif A == 31:  # WRITE_MEM
            B = binary_data[pc + 1]
            C = struct.unpack('>I', binary_data[pc + 2:pc + 6])[0]
            D = struct.unpack('>H', binary_data[pc + 6:pc + 8])[0]
            address = memory[B] + C
            memory[address] = memory[D]
            pc += 8
        elif A == 22:  # BSWAP
            B = binary_data[pc + 1]
            C = struct.unpack('>I', binary_data[pc + 2:pc + 6])[0]
            value = memory[B]
            swapped_value = (value >> 24) | ((value >> 8) & 0xFF00) | ((value << 8) & 0xFF0000) | (value << 24)
            memory[C] = swapped_value
            pc += 6

    result = {f'{i}': memory[i] for i in range(memory_range[0], memory_range[1] + 1)}

    with open(output_file, 'w') as f:
        yaml.dump({'memory': result}, f)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = list(map(int, sys.argv[3:5]))
    interpret(input_file, output_file, memory_range)
