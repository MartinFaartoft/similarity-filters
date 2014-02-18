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
		pass

class LocalitySensitiveHash:
	def __init__(self, indices_of_bits_to_sample):
		self.indices_of_bits_to_sample = indices_of_bits_to_sample

	def hash(self, element):
		pass

def calculate_hamming_distance(element, other_element):
	pass
