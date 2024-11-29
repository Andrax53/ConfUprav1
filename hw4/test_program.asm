# Test program to perform bswap on a vector of length 5
# Vector is stored starting at memory address 100

# Set up base address in register 0
load_const 0, 100

# Initialize vector with test values
# First element
load_const 1, 0x12345678
write_memory 0, 0, 1

# Second element
load_const 1, 0xAABBCCDD
write_memory 0, 1, 1

# Third element
load_const 1, 0x87654321
write_memory 0, 2, 1

# Fourth element
load_const 1, 0xFEDCBA98
write_memory 0, 3, 1

# Fifth element
load_const 1, 0x11223344
write_memory 0, 4, 1

# Read and bswap element at memory[100]
read_memory 2, 0, 0
bswap 2, 2
write_memory 0, 0, 2

# Read and bswap element at memory[101]
read_memory 2, 0, 1
bswap 2, 2
write_memory 0, 1, 2

# Read and bswap element at memory[102]
read_memory 2, 0, 2
bswap 2, 2
write_memory 0, 2, 2

# Read and bswap element at memory[103]
read_memory 2, 0, 3
bswap 2, 2
write_memory 0, 3, 2

# Read and bswap element at memory[104]
read_memory 2, 0, 4
bswap 2, 2
write_memory 0, 4, 2
