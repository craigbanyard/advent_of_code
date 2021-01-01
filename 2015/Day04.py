from time import time
from hashlib import md5

def check_hash(s,N):
    return md5(s.encode()).hexdigest()[0:N] == '0'*N

def day4(key,N):
    n = 1
    while(True):
        s = key + str(n)
        if check_hash(s,N):
            break
        n+=1
    return n

print("AoC 2015\nDay 4\n-----")
t0=time()
print("Part 1:",day4('bgvyzdsv',5))
print("Time:",time()-t0,"\n-----")
t0=time()
print("Part 2:",day4('bgvyzdsv',6))
print("Time:",time()-t0,"\n-----")

del t0