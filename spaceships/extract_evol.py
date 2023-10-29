import gdb
import numpy as np
from matplotlib import pyplot as plt

byte_width = 0x12
bit_width = 0x8e
height = 0x242

TOT_FRAMES = 300

res = input('input ? ')
#print(res)
#res = 'aaaaaaaa'

gdb.execute('file ./spaceships')
br = gdb.Breakpoint('strtoul@plt')
gdb.execute('r {}'.format(res))
addr_in_main = gdb.execute('bt', to_string=True).split('\n')[1].split()[1]
addr_check = int(addr_in_main[2:], base=16)-311
addr_epoch = addr_check-409
addr_interesting = addr_epoch+23

#gdb.execute('x/40i {}'.format(hex(addr_epoch)))
br2 = gdb.Breakpoint("*" + hex(addr_interesting))

for i in range(TOT_FRAMES):
    gdb.execute('c')
    map_mem = gdb.execute('i r rax', to_string=True).split()[1]
    gdb.execute('dump binary memory dumps/frame_{:03d}.bin {} {}'.format(i, map_mem, hex(int(map_mem[2:], base=16)+0x28c8)))

frames = []

for i in range(TOT_FRAMES):
    with open('dumps/frame_{:03d}.bin'.format(i), 'rb') as f:
        bit_array = []

        for x in range(height):
            row = f.read(byte_width)

            for i in range(bit_width):
                bit = row[i>>3] & (1 << (7-(i%8)))
                bit_array.append(bit!=0)

        frames.append(np.array(bit_array).reshape((height, bit_width)))

        fig = plt.figure(figsize=(bit_width//30,height//30))
        ax = fig.add_subplot(111)
        ax.imshow(frames[-1], aspect='auto', cmap=plt.cm.gray, interpolation='nearest')
        plt.show()

    #a = gdb.history(0).split('\n')
    #print(a)

