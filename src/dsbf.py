#TODO 
# read data

class DistanceSensitiveBloomFilter:
	
	#k = number of hash functions to use
	#m = length of each subarray/partition (equal to max output value from each hash function)
	def __init__(self, k, m):
		self.k = k
		self.m = m
		self.hash_functions = [] #make k of these
		self.bit_array = [[0] * m] * k	 #k 'rows' of length m

	#counts number of 'turned on' bits in the filter, looking only at positions
	#that 'element' hashes to
	def count_number_of_true_values(self, element):
		pass

	#hash element with k different hash functions, flip bit number [k, hash_functions[k](element)]
	def add_element(self, element):
		for i in range(self.k):
			hash_value = self.hash_functions[i](element)
			self.bit_array[hash_value][i] = 1


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