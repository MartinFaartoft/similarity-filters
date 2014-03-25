from dsbf import DistanceSensitiveBloomFilter
import random
import math


randBinList = lambda n: [random.randint(0, 1) for b in range(1, n+1)]

prime_100 = 2147483659

seed = random.randint(0, 100000)
length = 65536
number_of_elements = 1000
number_of_candidates = 10000

#Harvard pp. 44
# c = 1 if number of characters in the "alphabet" = 2
c = 1
epsilon = 0.1
delta = 0.4
k = 20

n = number_of_elements

base = (1 - c * epsilon) / float(1- c * delta)
# l_prime = number of bits to sample
l_prime = int(math.ceil(math.log(4 * n, base)))
# m_prime = Size of each of the k subarrays (total memory usage m = k * m_prime)
m_prime = 2 ** l_prime

threshold = (k * ((1 - c * epsilon) ** l_prime)) / 2

closeness = int(math.floor(length * epsilon))
farness = int(math.floor(length * delta))


#print "seed: " + str(seed)
#print "l_prime:", l_prime, "m_prime:", m_prime, "T:", threshold, closeness



def generate_close_candidates(candidate, min_distance, max_distance, number_of_candidates):
    """ candidate = candidate bit array
        close = number of bits to flip """
    #Generate bit mask
    random.seed(seed)
    zeroes = [0] * len(candidate)
    number_of_bits_to_flip = random.randint(min_distance, max_distance)
    #number_of_bits_to_flip = close
    for i in range(number_of_bits_to_flip):
        zeroes[i] = 1

    for i in range(number_of_candidates):
        random.shuffle(zeroes)
        copy = list(candidate)
        for u in range(len(zeroes)):
            if zeroes[u] == 1:
                copy[u] = 0 if copy[u] == 1 else 1
        yield copy


def populate_dsbf(dsbf, n, length):
    #TODO: Insert static random data
    for i in range(n):
        element = randBinList(length)
        dsbf.add_element(element)


def run():
    dsbf = DistanceSensitiveBloomFilter(k, m_prime, l_prime, prime_100, seed, threshold, length)
    candidate = randBinList(length)
    dsbf.add_element(candidate)
    populate_dsbf(dsbf, number_of_elements - 1, length)
    #print 'after populate'
    count_true = 0
    count_false = 0
    for close_element in generate_close_candidates(candidate, 0, closeness, number_of_candidates):
        #print dsbf.count_number_of_true_values(close_element)
        if dsbf.is_close(close_element):
            count_true += 1
        else:
            count_false += 1

    print "true positives: " + str(count_true)
    print "false negatives: " + str((number_of_candidates - count_true) / float(number_of_candidates))

    count_true = 0
    for far_element in generate_close_candidates(candidate, farness, length, number_of_candidates):
        if dsbf.is_close(far_element):
            count_true += 1

    print "true negatives: " + str(number_of_candidates - count_true)
    print "false positives: " + str((count_true) / float(number_of_candidates))



def pagh_graph():
    dsbf = DistanceSensitiveBloomFilter(k, m_prime, l_prime, prime_100, seed, threshold, length)
    candidate = randBinList(length)
    dsbf.add_element(candidate)
    populate_dsbf(dsbf, number_of_elements - 1, length)
    count_true = 0
    k_true_list = []
    for close_element in generate_close_candidates(candidate, closeness, number_of_candidates):
        k_true_list.append(dsbf.count_number_of_true_values(close_element))
    #for hash_func in dsbf.hash_functions:
        #print hash_func.indices_of_bits_to_sample

    k_true_list.sort()

    import json
    print json.dumps(k_true_list)








#pagh_graph()
run()

#def __init__(self, k, m, bits_to_sample, prime, seed):
