

def is_prime(value, know_primes=[]):
	'''
	Given a list of prime numbers, check if a number is a prime number
	'''
	if (max(know_primes)**2) > value:
		for prime in know_primes:
			if (value % prime) == 0:
				return False
		return True
	else:
		raise ValueError('List of known primes is too short for the given value')

def find_all_primes(ceil):
	'''
	find all prime numbers in a range, from 2 to "ceil"
	'''
	known_primes = [2, ]
	for i in range(3, ceil+1):
		if is_prime(i, known_primes):
			known_primes.append(i)

	return known_primes