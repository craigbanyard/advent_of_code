#=================#
# Day 22 AoC 2019 #
#=================#

from collections import deque
from time import time
from math import gcd

path = "F:\\Users\\Craig\\Documents\\Programming\\R\\Advent of Code\\Inputs\\Day22.txt"

# Parse input into list of shuffle instructions
def parse_input(path):
    shuffle = [line.rstrip('\n') for line in open(path).readlines()]
    # Create list of instructions and associated offsets
    S = []
    for i in shuffle:
        if i=='deal into new stack':
            S.append(i)
        else:
            a,b = i.rsplit(' ',1)
            S.append((a,int(b)))
    return S

# Parse test input (i.e. not from file)
def parse_test_input(test_input):
    shuffle = [line.rstrip('\n') for line in test_input]
    # Create list of instructions and associated offsets
    S = []
    for i in shuffle:
        if i=='deal into new stack':
            S.append(i)
        else:
            a,b = i.rsplit(' ',1)
            S.append((a,int(b)))
    return S

# Shuffle function (shuffles whole deck - cannot use for part 2 - memory)
def shuffle_deck(deck,process):
    cards = len(deck)
    for i in process:
        if i=='deal into new stack':
            # Reverse the order of the deck
            deck.reverse()
        elif i[0]=='cut':
            # Cut the deck at position n
            n = i[1]
            deck=deck[n:]+deck[:n]
        elif i[0]=='deal with increment':
            # Deal with increment n
            n = i[1]
            pos = 0
            orig_deck = deque(deck)
            while orig_deck:
                deck[pos]=orig_deck.popleft()
                if pos+n >= cards:
                    pos = (pos+n) % cards
                else:
                    pos+=n
        else:
            # Unexpected instruction
            assert False
    return deck

"""
Functions to return the new card position after a given shuffle instruction
Followed by function that applies all shuffle instructions to a single card

"""
# Deal into new stack
# f(x) = ax + b : a=-1, b=-1
def new_stack(deck_len,card_pos):
    return deck_len - card_pos - 1

# Cut n
# f(x) = ax + b : a=1, b=-n
def cut_n(deck_len,card_pos,n):
    return card_pos - n % deck_len

# Deal with increment n
# f(x) = ax + b : a=n, b=0
def inc_n(deck_len,card_pos,n):
    return n * card_pos % deck_len

# Shuffle single card using above shuffle functions
def shuffle_card(deck_len,process,card_pos):
    for i in process:
        if i=='deal into new stack':
            card_pos = new_stack(deck_len,card_pos)
        elif i[0]=='cut':
            card_pos = cut_n(deck_len,card_pos,i[1])
        elif i[0]=='deal with increment':
            card_pos = inc_n(deck_len,card_pos,i[1])
        else:
            # Unexpected instruction
            assert False
    return card_pos % deck_len

"""
The following functions make use of modular arithmetic
Observe that each shuffle instruction is a linear mapping of the form:
f(x) = ax + b mod D
where D is the number of cards in the deck and x is the card position
This function is called a linear congruential function (LCF)
See: https://en.wikipedia.org/wiki/Linear_congruential_generator
Now write a function get_lcf to return a and b for an input instruction

"""

# Return a,b in f(x) = ax + b mod D following above rules
def get_lcf(instruction):
    if instruction=='deal into new stack':
        a, b = -1, -1
    elif instruction[0]=='cut':
        a, b = 1, -instruction[1]
    elif instruction[0]=='deal with increment':
        a, b = instruction[1], 0
    else:
        # Unexpected instruction
        assert False
    return a, b

# Function to apply g(f(x)) and return new a,b
# f(x) = ax + b mod D
# g(x) = cx + d mod D
def reduce_lcfs(deck_len,f,g):
    a,b = f
    c,d = g
    # g(f(x)) = c(ax+b)+d mod D = acx+bc+d mod D => (a,b) = (ac mod D, bc+d mod D)
    return a*c % deck_len, (b*c + d) % deck_len
    
# Attempt to reduce process with modular arithmetic
def reduce_process(deck_len,process):
    # Cycle adjacent instructions, combine and reduce
    f = process[0]
    g = process[1]
    f = reduce_lcfs(deck_len,get_lcf(f),get_lcf(g))
    if len(process)>2:
        for g in process[2:]:
            f = reduce_lcfs(deck_len,f,get_lcf(g))
    return f

# Function to turn lcf into two shuffle insructions (increment then cut)
def lcf_to_inst(f):
    a,b = f
    p1 = 'deal with increment ' + str(a)
    p2 = 'cut ' + str(-b)
    return [p1,p2]

# Reduce process n times using exponentiation by squaring
# This is allowed because composing LCFs is an associative operation
def reduce_lcf_ntimes(deck_len,lcf,n):
    if n<0:
        assert False
    if n==0:
        return 1,0
    if n==1:
        return lcf
    if n%2==0:
        f = reduce_lcfs(deck_len, lcf, lcf)
        return reduce_lcf_ntimes(deck_len, f, n/2)
    else:
        f = reduce_lcfs(deck_len, lcf, lcf)
        f = reduce_lcf_ntimes(deck_len, f, (n-1)/2)
        return reduce_lcfs(deck_len, lcf, f)

# Compute x^y mod m
def power(x,y,m):
    if y==0:
        return 1
    p = power(x, y//2, m) % m
    p = (p*p) % m
    if y%2==0:
        return p 
    else:
        return (x*p) % m

# Modular multiplicative inverse using Fermat's Little Theorem
def mod_inv(a,m):
    g = gcd(a,m)
    if g != 1:
        # Inverse doesn't exist
        assert False
    return power(a, m-2, m)


# %% Original attempt (before reading part 2)
# t0 = time()

# # Shuffle factory order deck and find position of card 2019
# deck = list(range(10007))
# process = parse_input(path)
# card = 2019
# t1 = time()
# part1 = shuffle_deck(deck,process).index(card)
# t2 = time()

# print("Day 22")
# print("------")
# print("Pre-processing time:",t1-t0)
# print("------")
# print("Part 1:",part1)
# print("Time:  ",t2-t1)

# %% More efficient attempt at part 1 (after reading part 2)
# t0 = time()

# # Shuffle factory order deck and find position of card 2019
# deck_len = 10007
# process = parse_input(path)
# card = 2019
# t1 = time()
# part1 = shuffle_card(deck_len,process,card)
# t2 = time()

# print("Day 22")
# print("------")
# print("Pre-processing time:",t1-t0)
# print("------")
# print("Part 1:",part1)
# print("Time:  ",t2-t1)


# %% Part 1 with reduced process - even more efficient
t0 = time()

# Reduce input instructions and then apply new instructions
deck_len = 10007
f = reduce_process(deck_len,parse_input(path))
reduced_process = parse_test_input(lcf_to_inst(f))
card = 2019
t1 = time()
part1 = shuffle_card(deck_len,reduced_process,card)
t2 = time()

# Or even more trivially, simply apply the reduced LCF to the card position
# new_x = f(x) = ax + b mod deck_len
assert part1 == (f[0]*card + f[1]) % deck_len

# Check that the deck returns to original position after deck_len-1 shuffles
card_pos = card
for _ in range(deck_len-1):
    card_pos = (f[0]*card_pos + f[1]) % deck_len
assert card == card_pos

print("Day 22")
print("------")
print("Pre-processing time:",t1-t0)
print("------")
print("Part 1:",part1)
print("Time:  ",t2-t1)


# %% Part 2
t3 = time()

new_deck_len = 119315717514047
num_shuffles = 101741582076661
target_pos = 2020

# Get LCF of reduced process after applying num_shuffles times
# Only works because new_deck_len and num_shuffles are coprime:
# https://www.wolframalpha.com/input/?i=119315717514047+and+101741582076661+coprime
g = reduce_process(new_deck_len,parse_input(path))
g = reduce_lcf_ntimes(new_deck_len, g, num_shuffles)

# Need inverse of above LCF to find which card ends in position target_pos
# Let g(x) = ax + b mod D, we can then find the inverse, g'(x), by substitution:
# g(g'(x)) = x = a*g'(x) + b mod D => g'(x) = (x-b)/a mod D
# To divide in modular space, we require modular multiplicative inverse 1/a mod D = mod_inv(a,D)
# So the answer is (x - b) * mod_inv(a,D) mod D:
part2 = ((target_pos - g[1]) * mod_inv(g[0], new_deck_len)) % new_deck_len
t4 = time()

print("------")
print("Part 2:",part2)
print("Time:  ",t4-t3)
print("------")
print("Total execution time:",t4-t0)
del t0,t1,t2,t3,t4,card_pos,path
