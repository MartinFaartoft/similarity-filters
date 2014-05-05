from dsbf import DistanceSensitiveBloomFilter
import random
import math

#create random bit list of length n
randBinList = lambda n: [random.randint(0, 1) for b in range(1, n+1)]

prime_100 = 2147483659

seed = 98457198
random.seed(seed)

#number_of_elements = 1000
#number_of_candidates = 1000

#Harvard pp. 44
# c = 1 if number of characters in the "alphabet" = 2
#c = 1
#epsilon = 0.1
#delta = 0.4
#length = 65536
#k = 20 #number of hash functions
#n = number_of_elements

#closeness = int(math.floor(length * epsilon))
#farness = int(math.floor(length * delta))


def calculate_harvard_params(epsilon, delta, l, k, n):
    c = 1
    base = (1 - c * epsilon) / float(1- c * delta)
    # l_prime = number of bits to sample
    l_prime = int(math.ceil(math.log(4 * n, base)))
    # m_prime = Size of each of the k subarrays (total memory usage m = k * m_prime)
    m_prime = 2 ** l_prime
    threshold = (k * ((1 - c * epsilon) ** l_prime)) / 2

    space = m_prime*k
    total_input_size = n*l
    fraction = space / float(total_input_size)

    return epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction

def calculate_params_eliminate_false_negatives(epsilon, delta, l, k, n, l_prime):

    epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction = calculate_harvard_params(epsilon, delta, l, k, n)
    m_prime = 2 ** l_prime #2**l_prime #override harvard m_prime
    #print "epsilon, delta, l, k, n, l_prime, m_prime, threshold ", epsilon, delta, l, k, n, l_prime, m_prime, threshold
    print "space=", m_prime*k, "total input size=", n*l, "fraction=", m_prime*k / float(n*l)
    space = m_prime*k
    total_input_size = n*l
    fraction = space / float(total_input_size)

    """ epsilon_abs = absolute allowed hamming distance """
    epsilon_abs = math.ceil(l * float(epsilon))
    """ ln = The maximum number of times some bit in the element can be sampled """
    ln = math.ceil(k*l_prime / float(l))
    threshold = k - ln * epsilon_abs
    #print "threshold=",threshold,"ln=",ln,"epsilon_abs",epsilon_abs
    if (threshold <= 0):
        print "WAAARNNIINNGGG"
        #assert(threshold > 0)
    return epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction


def generate_close_candidates(candidate, min_distance, max_distance, number_of_candidates, wildcards=[]):
    zeroes = [0] * len(candidate)
    number_of_bits_to_flip = max_distance if min_distance == 0 else min_distance
    for i in range(number_of_bits_to_flip):
        zeroes[i] = 1

    for i in range(number_of_candidates):
        mask = list(zeroes)
        random.shuffle(mask)
        number_of_bits_to_resample = [mask[x] for x in wildcards].count(1)
        if number_of_bits_to_resample > 0:
            indices_to_choose = [u for u, y in enumerate(mask) if y == 0]
            #print number_of_bits_to_resample, len(indices_to_choose)

            flip_bits = random.sample(indices_to_choose, number_of_bits_to_resample)
            for v in flip_bits:
                mask[v] = 1

        copy = list(candidate)
        for u in range(len(zeroes)):
            if mask[u] == 1:
                copy[u] = 0 if copy[u] == 1 else 1
        yield copy


def populate_dsbf(dsbf, n, length):
    #TODO: Insert static random data
    for i in range(n):
        element = randBinList(length)
        dsbf.add_element(element)


def calculate_accuracy_ratios(dsbf, n, l, closeness, farness, number_of_candidates, wildcards=[]):
    candidate = randBinList(l)
    dsbf.add_element(candidate)
    populate_dsbf(dsbf, n - 1, l)

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for close_element in generate_close_candidates(candidate, 0, closeness, number_of_candidates, wildcards):
        is_close, stats = dsbf.is_close_wildcards(close_element, wildcards)
        if is_close:
            tp += 1
        else:
            fn += 1

    count_true = 0
    for far_element in generate_close_candidates(candidate, farness, l, number_of_candidates, wildcards):
        is_close, stats = dsbf.is_close_wildcards(far_element, wildcards)
        if is_close:
            fp += 1
        else:
            tn += 1

    tpr = tp / float(tp+fn)
    fnr = fn / float(tp+fn)
    fpr = fp / float(fp+tn)
    tnr = tn / float(fp+tn)

    return (tpr, fnr, fpr, tnr)

def pagh_graph():
    epsilon = 0.05
    delta = 0.4
    l = 65536
    n = 10000
    number_of_candidates = 1000
    closeness = int(math.floor(l * epsilon))
    farness = int(math.floor(l * delta))
    final_list = []
    for step_k in range(49,50):

        print step_k

        epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction = calculate_harvard_params(epsilon=epsilon, delta=delta, l=l, k=step_k, n=n)

        print threshold
        dsbf = DistanceSensitiveBloomFilter(k, m_prime, l_prime, prime_100, seed, threshold, l)
        candidate = randBinList(l)
        dsbf.add_element(candidate)
        populate_dsbf(dsbf, n - 1, l)
        count_true = 0
        k_true_list = []
        k_false_list = []


        for close_element in generate_close_candidates(candidate, 0, closeness, number_of_candidates):
            k_true_list.append(dsbf.count_number_of_true_values(close_element))

        for far_element in generate_close_candidates(candidate, farness, l, number_of_candidates):
            k_false_list.append(dsbf.count_number_of_true_values(far_element))

        k_true_list.sort()
        k_false_list.sort()

        final_list.append(k_true_list)
        final_list.append(k_false_list)

    import json
    print json.dumps(final_list)


def harvard_graph():
    epsilon = 0.1
    delta = 0.4
    l = 65536
    n = 1000
    number_of_candidates = 10000
    no_wildcards = 10

    wildcards = random.sample(range(l), no_wildcards)
    #wildcards = []

    closeness = int(math.floor(l * epsilon))
    farness = int(math.floor(l * delta))
    data = []

    for step_k in range(1, 30, 1):
        print "K=", step_k
        epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction = calculate_harvard_params(epsilon, delta, l, step_k, n)
        dsbf = DistanceSensitiveBloomFilter(k, m_prime, l_prime, prime_100, seed, threshold, l) #k, m, l_prime, prime, seed, threshold, length):

        data_row = calculate_accuracy_ratios(dsbf, n, l, closeness, farness, number_of_candidates, wildcards)
        data.append((k, data_row))

    import json

    with open('wildcard/harvard_graph_with_wildcards_%d.json' % no_wildcards, 'w') as outfile:
        json.dump(data, outfile)

def eliminate_false_negatives_experiment():
    epsilon = 0.05
    delta = 0.4
    l = 24000
    n = 1000
    number_of_candidates = 1000
    #step_k = 25
    l_prime = 11
    data_collection = []

    closeness = int(math.floor(l * epsilon))
    farness = int(math.floor(l * delta))
    for step_k in range(11, 75, 1):
        epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction = calculate_params_eliminate_false_negatives(epsilon=epsilon, delta=delta, l=l, k=step_k, n=n, l_prime=l_prime)
        #epsilon, delta, l, k, n, l_prime, m_prime, threshold, space, total_input_size, fraction = calculate_harvard_params(epsilon=epsilon, delta=delta, l=l, k=step_k, n=n)

        dsbf = DistanceSensitiveBloomFilter(k, m_prime, l_prime, prime_100, seed, threshold, l) #k, m, l_prime, prime, seed, threshold, length):

        data_row = calculate_accuracy_ratios(dsbf, n, l, closeness, farness, number_of_candidates)

        tpr, fnr, fpr, tnr = data_row
        new_data = (step_k, tpr, fnr, fpr, tnr, space)
        print step_k
        print "tpr, fnr, fpr, tnr"
        #assert(fnr == 0.0)
        print new_data
        data_collection.append(new_data)

    import json

    with open('eliminate_false_negatives_experiment.json', 'w') as outfile:
        json.dump(data_collection, outfile)


def test_generate_close():
    candidate = [1,1,1,1]
    wildcards = [2,3]
    min_distance = 2
    max_distance = 0
    number_of_candidates = 1

    list(generate_close_candidates(candidate, min_distance, max_distance, number_of_candidates, wildcards))

#pagh_graph()
#run()
harvard_graph()
#eliminate_false_negatives_experiment()
#def __init__(self, k, m, bits_to_sample, prime, seed):
#test_generate_close()
