import sys
import yaml
import struct

def assemble(input_file, output_file, log_file):
    commands = []
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            command = parts[0]
            args = [int(arg, 16) if arg.startswith('0x') else int(arg) for arg in parts[1:]]
            commands.append((command, args))

    binary_output = bytearray()
    log_output = []

    for command, args in commands:
        if command == 'LOAD_CONST':
            A, B, C = 82, args[0], args[1]
            binary_output.extend(struct.pack('>BBI', A, B, C))
            log_output.append({'command': 'LOAD_CONST', 'address': B, 'constant': C})
        elif command == 'READ_MEM':
            A, B, C, D = 19, args[0], args[1], args[2]
            binary_output.extend(struct.pack('>BBIH', A, B, C, D))
            log_output.append({'command': 'READ_MEM', 'address1': B, 'address2': C, 'offset': D})
        elif command == 'WRITE_MEM':
            A, B, C, D = 31, args[0], args[1], args[2]
            binary_output.extend(struct.pack('>BBIH', A, B, C, D))
            log_output.append({'command': 'WRITE_MEM', 'address1': B, 'offset': C, 'address2': D})
        elif command == 'BSWAP':
            A, B, C = 22, args[0], args[1]
            binary_output.extend(struct.pack('>BBI', A, B, C))
            log_output.append({'command': 'BSWAP', 'address1': B, 'address2': C})

    with open(output_file, 'wb') as f:
        f.write(binary_output)

    with open(log_file, 'w') as f:
        yaml.dump(log_output, f)

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    assemble(input_file, output_file, log_file)
