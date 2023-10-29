import pwn
import base64
import sys

SERVER_ADDRESS = 'instances.challenge-ecw.fr'
SERVER_PORT = 42471

with open(sys.argv[1], "rb") as f:
    program = f.read()

r = pwn.remote(SERVER_ADDRESS, SERVER_PORT)

r.sendline("-----PROGRAM START-----")
r.sendline(base64.b64encode(program))
r.sendline("-----PROGRAM END-----")

r.interactive()
