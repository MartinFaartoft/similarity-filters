# TODO generate random bitvectors (args: how long, how many) and pipe them to std::out

from sys import argv
import random
import json

array_length = int(argv[1])
no_of_arrays = int(argv[2])

arrays = []

for i in range(no_of_arrays):
    array = []
    for j in range(array_length):
        array.append(random.randint(0, 1))

    arrays.append(array)

print json.dumps(arrays)