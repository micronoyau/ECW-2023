from sys import argv

byte_width = 0x12
bit_width = 0x8e
height = 0x242

if len(argv) != 2:
    print("check_evol.py [dump file]")
    exit(0)


with open(argv[1], 'rb') as f:
    for x in range(height):
        row = f.read(byte_width)
        string = ''
        interpret = lambda x: ' ' if x==0 else 'O'
        for i in range(bit_width):
            bit = row[i>>3] & (1 << (7-(i%8)))
            string += interpret(bit)
        print(string)

