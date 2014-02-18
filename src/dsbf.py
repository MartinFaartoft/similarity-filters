import random 
class DistanceSensitiveBloomFilter:
	
	#k = number of hash functions to use
	#m = length of each subarray/partition (equal to max output value from each hash function)
	def __init__(self, k, m):
		self.k = k
		self.m = m
		self.hash_functions = self.prepare_hash_functions(k, m) #make k of these
		self.bit_array = [] 
		for i in range(k):
			self.bit_array.append([0] * m) 
			

	def prepare_hash_functions(self, k, m):
		hash_functions = []
		for i in range(k):
			p = 2147483659 #next after 2^31-1
			a = random.randint(1, p)
			b = random.randint(1, p)
			bits = random.sample(range(m), 5) #TODO replace 5 with the number of bits to sample
			lsh = LocalitySensitiveHash(bits, m, a, b, p)
			hash_functions.append(lsh)

		return hash_functions

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


randBinList = lambda n: [random.randint(0,1) for b in range(1,n+1)]


a = DistanceSensitiveBloomFilter(5,10)

#print a.bit_array
elem = randBinList(15)

a.add_element(elem)
a.add_element(randBinList(15))
a.add_element(randBinList(15))
a.add_element(randBinList(15))
a.add_element(randBinList(15))
a.add_element(randBinList(15))
a.add_element(randBinList(15))
a.add_element(randBinList(15))


print a.count_number_of_true_values(elem)
