from dsbf import DistanceSensitiveBloomFilter
import random

randBinList = lambda n: [random.randint(0, 1) for b in range(1, n+1)]

k = 10
m = 100
bits_to_sample = 5
prime_100 = 2147483659
seed = 9859028509821
threshold = 7


length = m

number_of_elements = 10
number_of_candidates = 10
closeness = threshold -1

own_seed = 8585


def generate_close_candidates(candidate, close, number_of_candidates):
    """ candidate = candidate bit array
        close = number of bits to flip """
    #Generate bit mask
    zeroes = [0] * len(candidate)
    for i in range(close):
        zeroes[i] = 1
    random.seed(seed)

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
        dsbf.add_element(randBinList(length))


def run():
    dsbf = DistanceSensitiveBloomFilter(k, m, bits_to_sample, prime_100, seed, threshold)
    populate_dsbf(dsbf, number_of_elements, length)
    candidate = randBinList(length)
    count_true = 0
    for close_element in generate_close_candidates(candidate, closeness, number_of_candidates):
        if dsbf.is_close(close_element):
            count_true += 1

    return count_true


print run()

#def __init__(self, k, m, bits_to_sample, prime, seed):