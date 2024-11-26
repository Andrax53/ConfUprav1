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

def interpreter(memory, program, start_addr=100, length=5):
    regs = [0] * 16  # General purpose registers
    pc = 0  # Program counter
    
    # Initialize test values in memory
    for i in range(length):
        memory[start_addr + i] = 0x12345678  # Example initial value
    
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
            if regs[addr] + offset < len(memory):
                regs[target] = memory[regs[addr] + offset]
            pc += 6
        elif cmd == 31:  # write_memory
            addr = (program[pc+1] >> 7) & 0x7FF
            offset = (program[pc+2] >> 3) & 0x3FF
            source = (program[pc+4] >> 5) & 0x7FF
            if regs[addr] + offset < len(memory):
                memory[regs[addr] + offset] = regs[source]
            pc += 6
        elif cmd == 22:  # bswap
            source = (program[pc+1] >> 7) & 0x7FF
            target = (program[pc+2] >> 3) & 0x7FF
            value = regs[source]
            regs[target] = ((value & 0xFF) << 24) | ((value & 0xFF00) << 8) | \
                          ((value & 0xFF0000) >> 8) | ((value & 0xFF000000) >> 24)
            pc += 4
        else:
            pc += 1  # Skip unknown commands
    
    # Generate result dictionary
    result = {"memory_values": {}}
    for i in range(length):
        addr = start_addr + i
        result["memory_values"][addr] = f"0x{memory[addr]:08X}"
    
    return result

if __name__ == "__main__":
    import sys
    import yaml
    
    if len(sys.argv) != 6:
        print("Usage: python uvm.py <input_asm> <output_bin> <log_file> <result_file> <memory_range>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]
    result_file = sys.argv[4]
    memory_range = [int(x) for x in sys.argv[5].split(',')]
    
    # Read assembly code
    with open(input_file, 'r') as f:
        code = []
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens = line.split()
            if line.endswith(':'):  # Label
                code.append((line,))
            else:
                try:
                    # Try to convert arguments to integers, skip if not possible (e.g., labels)
                    args = [int(x.strip(',')) for x in tokens[1:]]
                    code.append((tokens[0], *args))
                except ValueError:
                    # Skip lines that can't be converted to integers (like labels)
                    continue
    
    # Generate binary code
    binary = assembler(code)
    
    # Save binary output
    with open(output_file, 'wb') as f:
        f.write(binary)
    
    # Initialize memory and run interpreter
    memory = [0] * 1024  # 1024 memory locations
    start_addr, length = memory_range
    result = interpreter(memory, binary, start_addr, length)
    
    # Save log file
    log_data = {"instructions": []}
    pc = 0
    while pc < len(binary):
        cmd = binary[pc]
        if cmd == 82:  # load_const
            size = 4
            log_data["instructions"].append({
                "command": "load_const",
                "bytes": [f"0x{b:02X}" for b in binary[pc:pc+size]]
            })
        elif cmd in (19, 31):  # read_memory, write_memory
            size = 6
            log_data["instructions"].append({
                "command": "read_memory" if cmd == 19 else "write_memory",
                "bytes": [f"0x{b:02X}" for b in binary[pc:pc+size]]
            })
        elif cmd == 22:  # bswap
            size = 4
            log_data["instructions"].append({
                "command": "bswap",
                "bytes": [f"0x{b:02X}" for b in binary[pc:pc+size]]
            })
        pc += size
    
    with open(log_file, 'w') as f:
        yaml.dump(log_data, f, sort_keys=False)
    
    # Save result file
    with open(result_file, 'w') as f:
        yaml.dump(result, f, sort_keys=False)
