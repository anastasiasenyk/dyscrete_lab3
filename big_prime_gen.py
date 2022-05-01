"""Module to generate large prime numbers for RSA"""
import random

basic_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
					31, 37, 41, 43, 47, 53, 59, 61, 67,
					71, 73, 79, 83, 89, 97, 101, 103,
					107, 109, 113, 127, 131, 137, 139,
					149, 151, 157, 163, 167, 173, 179,
					181, 191, 193, 197, 199, 211, 223,
					227, 229, 233, 239, 241, 251, 257,
					263, 269, 271, 277, 281, 283, 293,
					307, 311, 313, 317, 331, 337, 347,
					349, 353, 359, 367, 373, 379, 383,
					389, 397, 401, 409, 419, 421, 431,
					433, 439, 443, 449, 457, 461, 463]

def get_possible_prime(n):
	'''Check if number is divided by simple primes'''
	while True:
		possible_prime = random.randrange(2**(n-1)+1, 2**n - 1)
		for num in basic_primes:
			if possible_prime % num == 0:
				break
		else: return possible_prime

def miller_rabin_test(num):
	'''Runs Miller-Rabin test for a lot of times (25)'''
	two_divisions = 0
	ec = num-1
	while ec % 2 == 0:
		ec >>= 1
		two_divisions += 1

	def prime_tester(round_tester):
		"""Additional function to test primality"""
		if pow(round_tester, ec, num) == 1:
			return False
		for i in range(two_divisions):
			if pow(round_tester, 2**i * ec, num) == num-1:
				return False
		return True

	for i in range(25):
		round_tester = random.randrange(2, num)
		if prime_tester(round_tester):
			return False
	return True

def prime_generator(bits_num=1024):
	"""Generates a prime number with given length"""
	while True:
		possible_prime = get_possible_prime(bits_num)
		if not miller_rabin_test(possible_prime):
			continue
		else:
			return possible_prime
