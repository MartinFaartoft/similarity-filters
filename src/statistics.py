from dsbf import DistanceSensitiveBloomFilter
import random
import math

randBinList = lambda n: [random.randint(0, 1) for b in range(1, n+1)]

prime_100 = 2147483659
seed = 9859028509821
length = 6400
number_of_elements = 10000
number_of_candidates = 1000
own_seed = 8585
#Harvard pp. 44
# c = Number of characters in the "alphabet"
c = 1
epsilon = 0.1
delta = 0.4
k = 10

n = number_of_elements

base = (1 - c * epsilon) / float(1- c * delta)
# l_prime = number of bits to sample
l_prime = int(math.ceil(math.log(4 * n, base)))
# m_prime = Size of each of the k subarrays (total memory usage m = k * m_prime)
m_prime = 2 ** l_prime

threshold = (k * ((1 - c * epsilon) ** l_prime)) / 2

closeness = int(math.floor(length * epsilon))

print "values", l_prime, m_prime, threshold, closeness

## Legeland
# k = 20
# length = 65536
# l_prime = 2
# m_prime = 2000
# threshold = 6
# closeness = 650

#Legeland end




def generate_close_candidates(candidate, close, number_of_candidates):
    """ candidate = candidate bit array
        close = number of bits to flip """
    #Generate bit mask
    random.seed(seed)
    zeroes = [0] * len(candidate)
    for i in range(close):
        zeroes[i] = 1


    for i in range(number_of_candidates):
        random.shuffle(zeroes)
        copy = list(candidate)
        for u in range(len(zeroes)):
            if zeroes[u] == 1:
                copy[u] = 0 if copy[u] == 1 else 0
        yield copy



def populate_dsbf(dsbf, n, length):
    #TODO: Insert static random data
    for i in range(n):
        element = randBinList(length)
        dsbf.add_element(element)


def run():
    dsbf = DistanceSensitiveBloomFilter(k, m_prime, l_prime, prime_100, seed, threshold, length)
    populate_dsbf(dsbf, number_of_elements, length)
    candidate = randBinList(length)
    count_true = 0
    for close_element in generate_close_candidates(candidate, closeness, number_of_candidates):
        print dsbf.count_number_of_true_values(close_element)
        if dsbf.is_close(close_element):
            count_true += 1
    return count_true


print run()

#def __init__(self, k, m, bits_to_sample, prime, seed):
