def assembler(code):
    bc = bytearray()
    labels = {}
    
    # First pass - collect labels
    current_pos = 0
    for op, *args in code:
        if isinstance(op, str) and op.endswith(':'):
            labels[op[:-1]] = current_pos
            continue
            
        if op == 'load_const':
            current_pos += 4
        elif op == 'read_memory':
            current_pos += 6
        elif op == 'write_memory':
            current_pos += 6
        elif op == 'bswap':
            current_pos += 4
            
    # Second pass - generate code
    for op, *args in code:
        if isinstance(op, str) and op.endswith(':'):
            continue
            
        if op == 'load_const':
            addr, const = args
            bc.extend(serializer(82, ((addr, 7), (const, 19)), 4))
        elif op == 'read_memory':
            target, addr, offset = args
            bc.extend(serializer(19, ((target, 7), (addr, 19), (offset, 31)), 6))
        elif op == 'write_memory':
            addr, offset, source = args
            bc.extend(serializer(31, ((addr, 7), (offset, 19), (source, 29)), 6))
        elif op == 'bswap':
            source, target = args
            bc.extend(serializer(22, ((source, 7), (target, 19)), 4))
            
    return bc

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, 'little')

def interpreter(memory, program):
    regs = [0] * 16  # General purpose registers
    pc = 0  # Program counter
    
    while pc < len(program):
        cmd = program[pc]
        if cmd == 82:  # load_const
            addr = (program[pc+1] >> 7) & 0x7FF
            const = (program[pc+2] >> 3) & 0x3FF
            regs[addr] = const
            pc += 4
        elif cmd == 19:  # read_memory
            target = (program[pc+1] >> 7) & 0x7FF
            addr = (program[pc+2] >> 3) & 0x7FF
            offset = (program[pc+4] >> 7) & 0x3FF
            regs[target] = memory[regs[addr] + offset]
            pc += 6
        elif cmd == 31:  # write_memory
            addr = (program[pc+1] >> 7) & 0x7FF
            offset = (program[pc+2] >> 3) & 0x3FF
            source = (program[pc+4] >> 5) & 0x7FF
            memory[regs[addr] + offset] = regs[source]
            pc += 6
        elif cmd == 22:  # bswap
            source = (program[pc+1] >> 7) & 0x7FF
            target = (program[pc+2] >> 3) & 0x7FF
            value = regs[source]
            regs[target] = ((value & 0xFF) << 24) | ((value & 0xFF00) << 8) | \
                          ((value & 0xFF0000) >> 8) | ((value & 0xFF000000) >> 24)
            pc += 4
    
    return memory

if __name__ == "__main__":
    import sys
    import yaml
    
    if len(sys.argv) != 4:
        print("Usage: python uvm.py <input_asm> <output_bin> <log_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    
    # Read assembly code
    with open(input_file, 'r') as f:
        code = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.endswith(':'):  # Label
                code.append(line)
                continue
            parts = line.replace(',', '').split()
            if len(parts) > 1:  # Instruction with arguments
                try:
                    args = [int(arg) for arg in parts[1:]]
                    code.append((parts[0], *args))
                except ValueError:
                    code.append((parts[0], *parts[1:]))  # Handle non-numeric arguments (like labels)
            else:  # Instruction without arguments
                code.append((parts[0],))
    
    # Assemble the code
    binary = assembler(code)
    
    # Write binary output
    with open(output_file, 'wb') as f:
        f.write(binary)
    
    # Write log file
    log = {'instructions': []}
    pos = 0
    for op, *args in code:
        if isinstance(op, str) and op.endswith(':'):
            continue
        instr_size = 4  # Default size
        if op in ['read_memory', 'write_memory']:
            instr_size = 6
        log['instructions'].append({
            'instruction': op,
            'args': args,
            'binary': list(binary[pos:pos+instr_size])
        })
        pos += instr_size
    
    with open(log_file, 'w') as f:
        yaml.dump(log, f, sort_keys=False)
