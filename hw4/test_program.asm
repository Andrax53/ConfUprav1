# Test program to perform bswap on a vector of length 5
# Vector is stored starting at memory address 100

# Read and bswap element at memory[100]
read_memory 2, 0, 100
bswap 2, 2
write_memory 0, 100, 2

# Read and bswap element at memory[101]
read_memory 2, 0, 101
bswap 2, 2
write_memory 0, 101, 2

# Read and bswap element at memory[102]
read_memory 2, 0, 102
bswap 2, 2
write_memory 0, 102, 2

# Read and bswap element at memory[103]
read_memory 2, 0, 103
bswap 2, 2
write_memory 0, 103, 2

# Read and bswap element at memory[104]
read_memory 2, 0, 104
bswap 2, 2
write_memory 0, 104, 2
