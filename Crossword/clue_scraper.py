
import string
import sys
import ast
import re
import puzzle_structure
import manipulate_clues

LONG_FILE_PATH = 'assets/clues-NEW.txt'
SHORT_FILE_PATH = 'assets/clues-short.txt'
FILE_PATH_1 = 'assets/clues-1.txt'
FILE_PATH_2 = 'assets/clues-2.txt'
FILE_PATH_3 = 'assets/clues-3.txt'
FILE_PATH_4 = 'assets/clues-4.txt'
FILE_PATH_5 = 'assets/clues-5.txt'
TO_IGNORE = [ 'the', 'a', 'an', 'of', 'with', 'and', 'in' ]
MIN_DISTANCE = 10

def main():
	puzzle_structure.read_raw_puzzle( puzzle_name )
	lookup_all_clues( puzzle_name )


def strip_puzzle_name( str ):
	"""
	@param: {string} str The name of the puzzle
	"""
	## strip file extension ##
	str.replace( '.txt', '' );
	## check for proper format ##
	if '/' in str:
		raise Exception( 'Incorrect format for puzzle_name. Should be DDMMYY.' )
	## return puzzle name ##
	return str


def lookup_all_clues( puzzle_name ):
	"""
	Look up all the clues for potential answers. Uses binary search and fuzzy search
	@param: {string} puzzle_name
	"""
	## load all clue lists into memory ##
	print( 'Loading clues...' )
	long_pairs = load_clues( LONG_FILE_PATH )
	pairs_1 = load_clues( FILE_PATH_1 )
	pairs_2 = load_clues( FILE_PATH_2 )
	pairs_3 = load_clues( FILE_PATH_3 )
	pairs_4 = load_clues( FILE_PATH_4 )
	pairs_5 = load_clues( FILE_PATH_5 )
	print( 'Done.' )

	## read current answers from answers.txt ##
	puzzle_name = strip_puzzle_name( puzzle_name )

	with open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt' ) as f:
		lines = f.read().splitlines()
	num_clues = len( lines ) - 3
	i = 0
	j = -1

	out_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'w' )

	out_file.write( '----------------------------------------------------\n')
	out_file.write( 'i\tj\tA/D\t\t[clue, pattern]\t\t\t\tanswers\n')
	out_file.write( '----------------------------------------------------\n')
	message = 'Computing answers'
	for line in lines:
		j += 1
		if ( j < 3 ):
			continue

		## parse the lines and look up the answers for each clue ##
		info = line.split( '\t' )
		clue = ast.literal_eval( info[3] )[0]
		pattern = ast.literal_eval( info[3] )[1]

		## figure out which list of shorter clues to use ##
		if len( pattern ) == 1:
			short_pairs = pairs_1
		elif len( pattern ) == 2:
			short_pairs = pairs_2
		elif len( pattern ) == 3:
			short_pairs = pairs_3
		elif len( pattern ) == 4:
			short_pairs = pairs_4
		else:
			short_pairs = pairs_5

		answers = lookup_single_clue( clue, pattern, long_pairs, short_pairs )
		out_file.write( info[0] + '\t' + info[1] + '\t' + info[2] + '\t' + str( info[3] ) + '\t' + str( answers ) + '\n' )

		sys.stdout.write( '\r                                ' )
		sys.stdout.write( '\r' + message + ( i % 4 )*'.' + ( 5 - i % 4 )*' ' + str( i + 1 ) + '/' + str( num_clues ) )
		sys.stdout.flush()
		i += 1

	out_file.close()
	print( '\nDone.' )


def lookup_single_clue( clue, pattern, long_pairs, short_pairs ):
	"""
	@param: {string} clue
	@param: {string} pattern The answer pattern so far
	@param: {string[]} long_pairs The clue/answer data
	@param: {string[]} short_pairs The clue/answer data partitioned by length
	@return: {string[]} A list of possible answers
	"""
	## try binary search, otherwise use fuzzy ##
	answers = binary_search( clue, pattern, long_pairs )
	if len( answers ) == 0:
		answers = fuzzy_search( clue, pattern, short_pairs )

	return answers


def binary_search( clue, pattern, pairs ):
	"""
	Perform standard binary search with incorporation of minimum edit distance
	@param: {string} clue
	@param: {string} pattern The answer pattern so far
	@param: {string[]} pairs The clue/answer data
	@return: {string[]} A list of possible answers
	"""
	clue = clue.lower()
	floor = 0
	ceiling = len( pairs ) - 1
	answers = []

	while floor <= ceiling:
		middle = ( floor + ceiling ) // 2
		cur_pair = ast.literal_eval( pairs[middle] )
		cur_clue = cur_pair[0].lower()
		if cur_clue > clue:
			ceiling = middle - 1
		elif cur_clue < clue:
			floor = middle + 1
		else:
			if len( cur_pair[1] ) == len( pattern ):
				answers = [ cur_pair[1] ]
			break
	if manipulate_clues.minimum_edit_distance( cur_clue, clue ) < MIN_DISTANCE and len( cur_pair[1] ) == len( pattern ):
		answers = [ cur_pair[1] ]
	return answers


def fuzzy_search( clue, pattern, pairs ):
	"""
	Perform a fuzzy regex search on the data. This is much slower than binary search
	@param: {string} clue
	@param: {string} pattern The answer pattern so far
	@param: {string[]} pairs The clue/answer data
	@return: {string[]} A list of possible answers
	"""
	answers = []
	key_words = clue.split()
	## extract key words ##
	key_words = [ word.strip( string.punctuation ) for word in key_words if word not in TO_IGNORE ]

	## leave clue as is if only composed of words from TO_IGNORE to avoid divide by 0 ##
	if len( key_words ) == 0:
		key_words = clue.split()

	## find answers that have a reasonable match with the clue ##
	for i, item in enumerate( pairs ):
		num_matches = 0
		num_missed = 0
		for word in key_words:
			if re.search( word, item, re.IGNORECASE ):
				num_matches += 1
			else:
				num_missed += 1
			if num_missed > len( key_words ) // 2:
				break

		if float( num_matches ) / len( key_words ) > .5:
			answer = ast.literal_eval( item )[1]
			if len( answer ) == len( pattern ) and answer not in answers:
				answers.append( answer )

	return answers

def load_clues( file_path ):
	"""
	@param: {string} file_path
	@return: {string[]} The clue/answer data
	"""
	clue_file = open( file_path, 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()
	return pairs


if __name__ == '__main__':
	# main()
	pass
