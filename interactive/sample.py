import pwn
import base64
import sys

SERVER_ADDRESS = "instances.challenge-ecw.fr"
SERVER_PORT = 42151

if len(sys.argv) != 2:
    print("Provide program to feed")
    exit(1)

#PROGRAM = "tests/2"
#PROGRAM = "prog.bin.1"
PROGRAM = sys.argv[1]

with open(PROGRAM, "rb") as f:
    program = f.read()

r = pwn.remote(SERVER_ADDRESS, SERVER_PORT)

print(r.recvline().decode()[:-1])
print(r.recvline().decode()[:-1])
print(r.recvline().decode()[:-1])
print(r.recvline().decode()[:-1])
print(r.recvline().decode()[:-1])

r.sendline(b"-----PROGRAM START-----")
r.sendline(base64.b64encode(program))
#r.sendline(base64.b64encode(bytes.fromhex('f824f93178')))
#r.sendline(base64.b64encode(bytes.fromhex('b024d9c73193f3f3fb686259')))
#r.sendline(base64.b64encode(bytes.fromhex('f824f93171a024923272b024cb3373859486e8247703')))
r.sendline(b"-----PROGRAM END-----")

r.interactive()
#print(r.recvall().decode())

