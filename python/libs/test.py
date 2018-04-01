#!/bin/env python3
import unittest

from mylib import is_prime
from mylib import find_all_primes

class TestMyLib(unittest.TestCase):
	def test_is_prime(self):
		self.assertEqual(is_prime(3, [2]), True)
		self.assertEqual(is_prime(4, [2, 3]), False)
		self.assertEqual(is_prime(5, [2, 3]), True)
		with self.assertRaises(ValueError):
			is_prime(9, [2])

	def test_find_all_primes(self):
		self.assertEqual(find_all_primes(2), [2])
		self.assertEqual(find_all_primes(10), [2, 3, 5, 7])


if __name__ == '__main__':
	unittest.main()