import sys
import re
import toml

def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Remove comments
    content = re.sub(r'\(comment.*?\)', '', content, flags=re.DOTALL)
    
    data = {}
    current_struct = None
    struct_count = 0
    
    # Split into lines and clean
    lines = [line.strip() for line in content.split('\n')]
    lines = [line for line in lines if line]  # Remove empty lines
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        try:
            # Parse constant declaration
            if '<-' in line:
                if not line.endswith(';'):
                    raise SyntaxError("Missing semicolon at end of constant declaration")
                
                # Split into name and value parts
                parts = line.split('<-', 1)
                if len(parts) != 2:
                    raise SyntaxError("Invalid constant declaration format")
                
                name = parts[0].strip()
                value = parts[1].strip()[:-1]  # Remove semicolon
                
                if not re.match(r'^[a-z][a-z0-9_]*$', name):
                    raise SyntaxError(f"Invalid constant name: {name}")
                
                # Handle constant evaluation
                if value.startswith('|') and value.endswith('|'):
                    const_name = value[1:-1].strip()
                    if const_name not in data:
                        raise ValueError(f"Undefined constant: {const_name}")
                    data[name] = data[const_name]
                else:
                    data[name] = eval_expression(value, data)
                
            # Parse struct
            elif line.startswith('struct {'):
                current_struct = {}
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('}'):
                    struct_line = lines[i].strip()
                    if struct_line:
                        if not struct_line.endswith(','):
                            raise SyntaxError(f"Missing comma in struct entry: {struct_line}")
                        entry_match = re.match(r'([a-z][a-z0-9_]*)\s*=\s*(.+),', struct_line)
                        if entry_match:
                            key, value = entry_match.groups()
                            current_struct[key] = eval_expression(value.strip(), data)
                        else:
                            raise SyntaxError(f"Invalid struct entry: {struct_line}")
                    i += 1
                if i >= len(lines) or not lines[i].strip().startswith('}'):
                    raise SyntaxError("Unclosed struct definition")
                
                # Store struct with unique name if there are multiple
                struct_name = f"struct{struct_count}" if struct_count > 0 else "struct"
                data[struct_name] = current_struct
                struct_count += 1
                current_struct = None
            
        except Exception as e:
            raise type(e)(f"Error on line {i + 1}: {str(e)}\nLine content: {line}")
        
        i += 1
    
    return data

def eval_expression(expr, data):
    expr = expr.strip()
    
    try:
        # Handle arrays
        if expr.startswith('[') and expr.endswith(']'):
            array_content = expr[1:-1].strip()
            if not array_content:
                return []
            return array_content.split()
            
        # Handle numbers
        if expr.isdigit():
            return int(expr)
            
        # Handle structs
        if expr.startswith('struct {') and expr.endswith('}'):
            struct_content = expr[7:-1].strip()
            struct_data = {}
            if struct_content:
                entries = [e.strip() for e in struct_content.split(',') if e.strip()]
                for entry in entries:
                    key, value = entry.split('=')
                    struct_data[key.strip()] = eval_expression(value.strip(), data)
            return struct_data
            
        # Handle constant references
        if expr in data:
            return data[expr]
            
        # Handle strings (anything else)
        return expr
            
    except Exception as e:
        raise ValueError(f"Error evaluating expression '{expr}': {str(e)}")

def write_toml(data, output_path):
    with open(output_path, 'w') as file:
        toml.dump(data, file)

def main():
    if len(sys.argv) != 3:
        print("Usage: python config_parser.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        data = parse_file(input_file)
        write_toml(data, output_file)
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
