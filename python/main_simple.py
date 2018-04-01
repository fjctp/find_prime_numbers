#!/bin/env python3

import argparse
from libs import mylib

def parse_args():
	parser = argparse.ArgumentParser(
		description='Find all prime number in a range (from 2).')
	parser.add_argument('max', type=int, default=1000,
	                    help='from 2 to MAX')

	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()

	known_primes = mylib.find_all_primes(args.max)

	print(known_primes)