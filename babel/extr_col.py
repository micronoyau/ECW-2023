import numpy as np

arr = np.genfromtxt('unknown.txt', dtype=str)

res = ''
for l in arr:
    res += ''.join(l)

print(res)
