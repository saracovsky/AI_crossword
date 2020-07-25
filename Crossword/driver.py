'''
TODO:
- improve performance with uncompressed data X
- improve performance with custom scraped data X
- partition wiki data X
- improve binary search to check surrounding answers
- add wikipedia search

LIMITATIONS:
- wordplay/humor
- in-puzzle references
- multiple letters per square / non-alphanumeric characters
- rich text (accents, etc)
'''

import os
import sys
import puzzle_solver
import evaluate

def main():
	puzzle_solver.fill( puzzle_name )
	diff = evaluate.compare_results( puzzle_name )
	evaluate.score_puzzle( diff )

if __name__ == '__main__':
	main()
