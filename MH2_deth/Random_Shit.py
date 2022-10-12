import random


def nBitRandom(n):

	# Returns a random number
	# between 2**(n-1)+1 and 2**n-1'''
	return(random.randrange(2**(n-1)+1, 2**n-1))


print(nBitRandom(50))

#1042356186582901
#660469632329893

# TLS HELP
#https://tls12.xargs.org/