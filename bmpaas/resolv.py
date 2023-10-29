from base64 import b85encode, b85decode
import base64
import socket
from matplotlib import pyplot as plt
from sys import argv
from tqdm import tqdm
import os
from signal import signal, SIGINT
from time import sleep

CHARSET = base64._b85alphabet.decode()
N = len(CHARSET)

HOST = 'instances.challenge-ecw.fr'
PORT = 41007
CIPHER_LEN = 2198
TOTAL_LEN = 2222

"""
if len(argv) != 3:
    print("Usage : {} [position] [count]".format(argv[0]))
    exit(1)
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(s.recv(1024).decode())

def guess_bytes(rounds):
    guess = []
    for i in range(CIPHER_LEN):
        guess.append([0] * 85)

    for rnd in tqdm(range(rounds)):
        s.send(b'1\n')
        ciphertext = s.recv(4096).decode()

        if len(ciphertext) != TOTAL_LEN:
            print("Received block of bad size")
            s.recv(8092)
            continue

        for pos in range(CIPHER_LEN):
            #print(pos)
            guess[pos][CHARSET.find(ciphertext[pos])] += 1


    res = ""
    for pos in range(CIPHER_LEN):
        res += CHARSET[guess[pos].index(max(guess[pos]))]

    print("Guess : ")
    print(res)


#rounds = 50000
#plt.plot(list(map(lambda x: x/rounds, probs(rounds))))
#plt.show()


"""
s.send(b'1\n')
ciphertext = s.recv(4096).decode()
print(len(ciphertext))

"""

cleartext = b"LQUQV00000004>r004Xd003(M000F5000317ytkO002}5000vU000vU000000000000000{{R600093000000002TqQgZ+R00000000000000000000000000000000000000000000000000000000006200000000000000000000000000000000960|NsC000000000000RR90|NsC0|Nj600RR9000030|NsC0|NsC0|Ns90000000RR9000000000000RR90|NsC0|Nj6000000|NsC0|Nj600000000030|NsC0{{R3000000000000RR9000030|NsC0{{R30|NsC0|Nj600RR90|Ns90000000RR90|NsC0|Nj600000000030|NsC0{{R300000000960{{R30|NsC0|Nj6000000|NsC0|Nj60000000000000960{{R300000000960|NsC000030|NsC0{{R300000000960{{R300000000960|NsC0000000000000000|NsC0|Nj600RR9000030|Nj6000000|Ns90000000RR90|NsC0|NsC0{{R30|NsC0|NsC0|NsC0|Ns9000960{{R30|Ns9000960|NsC0|Ns9000960|NsC000030|NsC0{{R30|Ns9000960|NsC000030|NsC0|NsC0|Ns9000960|NsC0|NsC0|NsC0|NsC000030|NsC0{{R30|NsC0|Nj600RR9000030|NsC0{{R30|Ns9000960|NsC000030|Nj600RR90|Ns9000960{{R30|Ns9000960|NsC000030|NsC0|NsC0|NsC0|NsC0{{R30|NsC0|Nj600RR9000030|Nj600RR90|Ns9000960|NsC0|Ns90000000RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0{{R30|Ns90000000000000030|NsC0{{R30|NsC0|NsC0|NsC000030|NsC0{{R30|NsC0|Nj600RR900000000960|NsC000030|NsC0{{R30|NsC0|Nj6000000|NsC0|Nj600000000030|NsC0|NsC0|NsC0|NsC0|NsC000030|NsC0{{R30|NsC0|Nj600RR9000030|NsC0{{R30|Ns9000960|NsC000030|Nj600RR90|Ns9000960{{R30|Ns9000960|NsC000030|NsC0|NsC0|NsC0|NsC0{{R30|NsC0|Nj600RR9000030|Nj600RR90|Ns9000960{{R3000030|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nj600RR9000030|NsC0{{R3000000000000RR90|NsC0|NsC0{{R30|NsC0|NsC0|NsC000030|NsC0|NsC0|NsC0|Nj600RR90|Ns9000960|NsC000000000000RR90|Ns9000960|NsC000030|Nj600RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC000000000000RR900000000960|NsC0|Ns90000000RR90|NsC0|Nj600000000030|Nj600RR90|Ns9000960{{R30|NsC0|Nj6000000|NsC0|NsC0|NsC0|NsC0|NsC0{{R300000000960|NsC0|NsC0|NsC0{{R300000000960|NsC000000000000RR90|NsC0|NsC0|NsC0|NsC0|Nj600RR9000030|NsC0{{R30|Ns9000000000000000000960|NsC000000000000RR9000030|NsC0|NsC0|NsC0|Nj600RR90|Ns90000000RR9000030|NsC0|NsC0|NsC0|Nj6000000|NsC0|Nj60000000000000960|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC000030|NsC0|NsC0|NsC0|NsC0{{R30|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0{{R30|NsC0|NsC0|NsC000030|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nj600RR9000030|Nj6000000|Ns90000"
with open("img.bmp", "wb") as f:
    f.write(base64.b85decode(cleartext))
#cleartext = cleartext.decode()

#guess_bytes(200000)

"""
for i in range(len(cleartext), len(ciphertext)):
    guessed = guess_byte(i, 25000)
    print("i={} : {}".format(i, guessed))
    cleartext += guessed
    sleep(1)
"""


"""
#expected_header = b'LQMbw0i6H<00000'
CIPHER_LEN = 2198
HEADER_LEN = 26
CONTENT_LEN = CIPHER_LEN//5 - HEADER_LEN

HEADER = b'BM' + CONTENT_LEN.to_bytes(4) + b'\x00\x00\x00\x00' + HEADER_LEN.to_bytes(4)

print(b85encode(HEADER).decode())
"""

