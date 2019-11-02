from random import random
import sys

minimum_cost = int(sys.argv[1])
maximum_cost = int(sys.argv[2])
n = int(sys.argv[3])

f = open(f"T_AISearchfile{n}.txt", 'w')

f.write(f"NAME = T_AISearchfile{n},\n")
f.write(f"SIZE = {n},")

for i in range(n-1):
    f.write("\n")
    for x in range(n-1-i):
        c = int(minimum_cost + random() * (maximum_cost - minimum_cost))
        f.write(f'{c},')

f.close()