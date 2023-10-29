from pwn import *

#conn = remote('instances.challenge-ecw.fr', 34982)
conn = remote('instances.challenge-ecw.fr', 35015)

ans = []

# Question 1

print(conn.recvline())

def q1():
    ans.append(b'yes')
    conn.sendline(ans[-1])

def q2():
    ans.append(b'42')
    conn.sendline(ans[-1])

def q3(prompt):
    letter = prompt.strip().split(":")[1][1:]

    if ('before' in prompt):
        choice = chr(ord(letter)-1)
        ans.append(choice.encode())
        conn.sendline(ans[-1])

    elif ('after' in prompt):
        choice = chr(ord(letter)+1)
        ans.append(choice.encode())
        conn.sendline(ans[-1])

def q4(prompt):
    color = list(map(int, prompt.strip().split(':')[1][1:].split(',')))
    if color == [0,0,0]:
        ans.append(b'black')
        conn.sendline(ans[-1])
    elif color == [0,0,255]:
        ans.append(b'blue')
        conn.sendline(ans[-1])
    elif color == [0,255,0]:
        ans.append(b'green')
        conn.sendline(ans[-1])
    elif color == [255,0,0]:
        ans.append(b'red')
        conn.sendline(ans[-1])
    elif color == [255,255,255]:
        ans.append(b'white')
        conn.sendline(ans[-1])


def q5(prompt):
    res = ','.join(map(lambda x: x.decode(), ans))
    conn.sendline(res.encode())

s1 = conn.recvline().decode()
print(s1)
q1()

# Question 2
s2 = conn.recvline().decode()
print(s2)
q2()

s3 = conn.recvline().decode()
print(s3)
q3(s3)

s4 = conn.recvline().decode()
print(s4)
q4(s4)
print(conn.recvline()) # Flag 1

# Step 5
s5 = conn.recvline().decode()
print(s5)
q5(s5)

# Step 6
prompt = conn.recvline().decode()
print(prompt)
tosend = list(map(int, prompt[78:].split(' ')[0].split(',')))

answer = []
for i in tosend:
    answer.append(ans[i-1].decode())
answer = (','.join(map(str, answer))).encode()
conn.sendline(answer)

# Step 7
s7 = conn.recvline().decode().split(':')[1][1:]
print(s7)

if s7.startswith('Do you wanna play'):
    q1()
elif s7.startswith('What is the meaning'):
    q2()
elif s7.startswith('Can you tell me what color '):
    q4(s7)
elif s7.startswith('I forgot everything'):
    q5()

print(conn.recvline())
