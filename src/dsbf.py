import random
class DistanceSensitiveBloomFilter:

	#k = number of hash functions to use
	#m = length of each subarray/partition (equal to max output value from each hash function)
	def __init__(self, k, m, l_prime, prime, seed, threshold, length):
		self.k = k
		self.m = m

		self.l_prime = l_prime
		self.seed = seed
		self.prime = prime
		self.length = length
		self.bit_array = []
		self.threshold = threshold
		random.seed(self.seed)

		self.prepare_bits_to_sample()
		self.hash_functions = self.prepare_hash_functions(k, m) #make k of these

		for i in range(k):
			self.bit_array.append([0] * m)

	def prepare_hash_functions(self, k, m):
		hash_functions = []

		for i in range(k):
			a = random.randint(1, self.prime)
			b = random.randint(1, self.prime)
			bits = self.bucket_of_bits_to_sample[i]
			lsh = LocalitySensitiveHash(bits, m, a, b, self.prime)
			hash_functions.append(lsh)

		return hash_functions

	def prepare_bits_to_sample(self):
		l_prime = self.l_prime
		bits = range(self.length)
		bucket_of_bits_to_sample = []

		while len(bucket_of_bits_to_sample) < self.k:
			random.shuffle(bits)
			for i in range(self.length / l_prime):
				chunk = bits[i * l_prime : i * l_prime + l_prime]
				if len(chunk) != l_prime:
					continue
				bucket_of_bits_to_sample.append(chunk)
		self.bucket_of_bits_to_sample = bucket_of_bits_to_sample

	#counts number of 'turned on' bits in the filter, looking only at positions
	#that 'element' hashes to
	def count_number_of_true_values(self, element):
		number_of_trues = 0
		for i in range(self.k):
			hash_value = self.hash_functions[i].hash(element)
			if self.bit_array[i][hash_value] == 1:
				number_of_trues += 1
		return number_of_trues

	#hash element with k different hash functions, flip bit number [k, hash_functions[k](element)]
	def add_element(self, element):
		for i in range(self.k):
			hash_value = self.hash_functions[i].hash(element)
			self.bit_array[i][hash_value] = 1

	def is_close(self, element):
		return self.threshold <= self.count_number_of_true_values(element)

class LocalitySensitiveHash:
	def __init__(self, indices_of_bits_to_sample, max_output, a, b, p):
		self.indices_of_bits_to_sample = indices_of_bits_to_sample
		self.max_output = max_output
		self.a = a
		self.b = b
		self.p = p

	def hash(self, element):
		sampled_bits = [element[i] for i in self.indices_of_bits_to_sample]
		integer_value = self.lsh_to_integer(sampled_bits)
		hash_value = self.hash_integer(integer_value)
		return hash_value

	def lsh_to_integer(self, lsh):
		powers = [2 ** i for i in range(len(lsh))][::-1]
		return sum([x*powers[i] for i,x in enumerate(lsh)])

	def hash_integer(self, x):
		return ((self.a * x + self.b) % self.p) % self.max_output

def calculate_hamming_distance(element, other_element):
	return sum([abs(pair[0]-pair[1]) for pair in zip(element, other_element)])