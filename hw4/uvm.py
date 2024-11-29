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
            bc.append(82)  # opcode
            bc.append(addr & 0xF)  # register
            bc.append(const & 0xFF)  # low byte
            bc.append((const >> 8) & 0xFF)  # high byte
        elif op == 'read_memory':
            target, addr, offset = args
            bc.append(19)  # opcode
            bc.append(target & 0xF)  # target register
            bc.append(addr & 0xF)  # address register
            bc.append(offset & 0xFF)  # offset
            bc.append(0)  # padding
            bc.append(0)  # padding
        elif op == 'write_memory':
            addr, offset, source = args
            bc.append(31)  # opcode
            bc.append(addr & 0xF)  # address register
            bc.append(offset & 0xFF)  # offset
            bc.append(source & 0xF)  # source register
            bc.append(0)  # padding
            bc.append(0)  # padding
        elif op == 'bswap':
            source, target = args
            bc.append(22)  # opcode
            bc.append(source & 0xF)  # source register
            bc.append(target & 0xF)  # target register
            bc.append(0)  # padding
            
    return bc

def serializer(cmd, fields, size):
    result = bytearray(size)
    result[0] = cmd
    
    for value, shift in fields:
        byte_index = 1 + (shift // 8)
        bit_shift = shift % 8
        if byte_index < size:
            result[byte_index] |= (value & 0xFF) << bit_shift
    
    return result

def interpreter(memory, program, start_addr=100, length=5, input_file='test_program.asm'):
    regs = [0] * 16  # General purpose registers
    pc = 0  # Program counter
    
    # Initialize test values in memory from input file
    initial_values = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.strip().startswith('load_const'):
                # Extract the hexadecimal value after the comma
                value = int(line.split(',')[1].split('#')[0].strip(), 16)
                initial_values.append(value)
    
    # Use only the first 'length' values
    for i in range(length):
        memory[start_addr + i] = initial_values[i]
    
    while pc < len(program):
        cmd = program[pc]
        if cmd == 82:  # load_const
            addr = program[pc+1] & 0xF
            const = (program[pc+2] | (program[pc+3] << 8))  # Get 16-bit constant
            regs[addr] = const
            print(f"Loading constant {const} into register {addr}")
            pc += 4
        elif cmd == 19:  # read_memory
            target = program[pc+1] & 0xF
            addr = program[pc+2] & 0xF
            offset = program[pc+3]
            addr_val = regs[addr] + offset
            if addr_val < len(memory):
                regs[target] = memory[addr_val]
                print(f"Reading from memory[{addr_val}]: 0x{regs[target]:08X}")
            pc += 6
        elif cmd == 31:  # write_memory
            addr = program[pc+1] & 0xF
            offset = program[pc+2]
            source = program[pc+3] & 0xF
            addr_val = regs[addr] + offset
            if addr_val < len(memory):
                memory[addr_val] = regs[source]
                print(f"Writing to memory[{addr_val}]: 0x{regs[source]:08X}")
            pc += 6
        elif cmd == 22:  # bswap
            source = program[pc+1] & 0xF
            target = program[pc+2] & 0xF
            value = regs[source]
            print(f"BSWAP: value before = 0x{value:08X}")
            # Swap bytes
            b0 = (value >> 24) & 0xFF
            b1 = (value >> 16) & 0xFF
            b2 = (value >> 8) & 0xFF
            b3 = value & 0xFF
            regs[target] = (b3 << 24) | (b2 << 16) | (b1 << 8) | b0
            print(f"BSWAP: value after = 0x{regs[target]:08X}")
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
    result = interpreter(memory, binary, start_addr, length, input_file)
    
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
