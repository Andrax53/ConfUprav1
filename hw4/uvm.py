import yaml
import sys
import unittest

def assembler(code):
    bc = []
    for op, *args in code:
        if op == 'move':
            b, c = args
            bc += serializer(82, ((b, 7), (c, 19)), 4)
        elif op == 'read':
            b, c, d = args
            bc += serializer(19, ((b, 7), (c, 19), (d, 31)), 6)
        elif op == 'write':
            b, c, d = args
            bc += serializer(31, ((b, 7), (c, 19), (d, 29)), 6)
        elif op == 'bswap':
            b, c = args
            bc += serializer(22, ((b, 7), (c, 19)), 4)
    return bc

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, 'little')

def interpreter(cmds):
    memory = [0] * 1024  # Предположим, что память имеет размер 1024 байта
    log = []
    for op, *args in cmds:
        if op == "move":
            address, const = args
            memory[address] = const
            log.append({'op': 'move', 'A': f'0x{82:02X}', 'B': f'0x{address:02X}', 'C': f'0x{const:02X}'})
        elif op == "write":
            target, source, offset = args
            memory[memory[target] + offset] = memory[source]
            log.append({'op': 'write', 'A': f'0x{31:02X}', 'B': f'0x{target:02X}', 'C': f'0x{source:02X}', 'D': f'0x{offset:02X}'})
        elif op == "read":
            b, c, d = args
            memory[c] = memory[memory[b] + d]
            log.append({'op': 'read', 'A': f'0x{19:02X}', 'B': f'0x{b:02X}', 'C': f'0x{c:02X}', 'D': f'0x{d:02X}'})
        elif op == "bswap":
            b, c = args
            memory[c] = int.from_bytes(memory[b].to_bytes(4, 'little'), 'big')
            log.append({'op': 'bswap', 'A': f'0x{22:02X}', 'B': f'0x{b:02X}', 'C': f'0x{c:02X}'})
    return log

def log_assembler(code, log_path):
    log = []
    for op, *args in code:
        log.append({'op': op, 'args': args})
    with open(log_path, 'w') as f:
        yaml.dump(log, f)

def log_interpreter(log, result_path):
    with open(result_path, 'w') as f:
        yaml.dump(log, f)

def read_commands(file_path):
    commands = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            op = parts[0]
            args = list(map(int, parts[1:]))
            commands.append((op, *args))
    return commands

def main(input_file, assembler_log, interpreter_result):
    commands = read_commands(input_file)
    log_assembler(commands, assembler_log)
    log = interpreter(commands)
    log_interpreter(log, interpreter_result)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run_uvm.py <input_file> <assembler_log> <interpreter_result>")
        sys.exit(1)

    input_file = sys.argv[1]
    assembler_log = sys.argv[2]
    interpreter_result = sys.argv[3]

    main(input_file, assembler_log, interpreter_result)
