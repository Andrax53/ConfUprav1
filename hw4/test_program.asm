# Test program to perform bswap on a vector of length 5
# Vector is stored starting at memory address 100

# Initialize vector length in register 0
load_const 0, 5

# Initialize counter in register 1
load_const 1, 0

loop_start:
    # Read vector element from memory[100 + counter]
    read_memory 2, 1, 100
    
    # Perform bswap on the element
    bswap 2, 2
    
    # Write result back to memory
    write_memory 1, 0, 2
    
    # Increment counter
    load_const 2, 1
    add 1, 1, 2
    
    # Compare counter with length
    cmp 1, 0
    jl loop_start
