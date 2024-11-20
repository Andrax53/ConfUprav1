import sys
import re
import toml

def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = {}
    current_table = None
    for line in lines:
        line = line.strip()
        if line.startswith("'"):
            continue  # Пропускаем однострочные комментарии
        elif line.startswith("var "):
            var_match = re.match(r'var (\w+) (.+);', line)
            if var_match:
                name, value = var_match.groups()
                data[name] = eval_expression(value)
        elif line.startswith("#("):
            array_match = re.match(r'#\((.+)\)', line)
            if array_match:
                values = array_match.group(1).split(',')
                data['array'] = [eval_expression(v.strip()) for v in values]
        elif line.startswith("table(["):
            if current_table:
                data['table'] = current_table
            current_table = {}
        elif line.endswith("])"):
            if current_table:
                data['table'] = current_table
                current_table = None
        elif current_table is not None:
            entry_match = re.match(r'(\w+) = (.+)', line)
            if entry_match:
                key, value = entry_match.groups()
                current_table[key.strip()] = eval_expression(value.strip())
        else:
            print(f"Syntax error: {line}")

    return data

def eval_expression(expr):
    if expr.isdigit():
        return int(expr)
    elif expr.startswith("@{"):
        return eval_constant_expression(expr)
    elif expr.startswith("#("):
        array_match = re.match(r'#\((.+)\)', expr)
        if array_match:
            values = array_match.group(1).split(',')
            return [eval_expression(v.strip()) for v in values]
    elif expr.startswith("table(["):
        table_match = re.match(r'table\(\[(.+)\]\)', expr, re.DOTALL)
        if table_match:
            entries = table_match.group(1).split(',')
            table_data = {}
            for entry in entries:
                key, value = entry.split('=')
                table_data[key.strip()] = eval_expression(value.strip())
            return table_data
    else:
        return expr.strip('"')

def eval_constant_expression(expr):
    expr = expr[2:-1]  # Удаляем @{ и }
    tokens = expr.split()
    if tokens[0] == '+':
        return eval_expression(tokens[1]) + eval_expression(tokens[2])
    elif tokens[0] == '-':
        return eval_expression(tokens[1]) - eval_expression(tokens[2])
    elif tokens[0] == '*':
        return eval_expression(tokens[1]) * eval_expression(tokens[2])
    elif tokens[0] == 'min':
        return min(eval_expression(tokens[1]), eval_expression(tokens[2]))
    elif tokens[0] == 'max':
        return max(eval_expression(tokens[1]), eval_expression(tokens[2]))
    else:
        raise ValueError(f"Unknown operation: {tokens[0]}")

def write_toml(data, output_path):
    with open(output_path, 'w') as file:
        toml.dump(data, file)

def main():
    if len(sys.argv) != 3:
        print("Usage: python config_parser.py <input_file> <output_file>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    data = parse_file(input_file)
    write_toml(data, output_file)

if __name__ == "__main__":
    main()
