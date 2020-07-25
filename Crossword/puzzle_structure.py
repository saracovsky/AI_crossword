
import clue_scraper
import ast

def read_raw_puzzle( puzzle_name ):
	"""
	@param: {string} puzzle_name The name of the puzzle
	"""
	puzzle_name = clue_scraper.strip_puzzle_name( puzzle_name )
	in_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-clues.txt', 'r' )
	out_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'w' )

	## write file header ##
	out_file.write( '----------------------------------------------------\n')
	out_file.write( 'i\tj\tA/D\t\t[clue, pattern]\t\t\t\tanswers\n')
	out_file.write( '----------------------------------------------------\n')
	for line in in_file:

		if ( line[2:8] == 'ACROSS' ):
			direction = 'across'
		elif( line[2:6] == 'DOWN' ):
			direction = 'down'
		elif ( line[0] == '#' or line[0] == '' ):
			continue
		else:
			info = line.split( '\t' )
			out_file.write( info[1] + '\t' + info[2] + '\t' + direction + '\t' + \
				str( [ info[4].strip(), '?' * int( info[3] ) ] ) + '\t' + str([]) + '\n' )

	in_file.close()
	out_file.close()


def sort_answers( puzzle_name ):
	"""
	Sort answers by weight of the first (most likely) answer

	@param: {string} puzzle_name
	"""
	puzzle_name = clue_scraper.strip_puzzle_name( puzzle_name )
	answer_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'r' )
	unsorted_answers = []
	sorted_answers = []
	i = -1

	## parse unsorted data ##
	for line in answer_file:
		i += 1
		if i < 3: #ignore header
			continue
		info = line.strip().split( '\t' )
		info[4] = ast.literal_eval( info[4] )
		unsorted_answers.append( info )

	answer_file.close()

	## sort it ##
	sorted_answers = sorted( unsorted_answers, cmp=compare_answers )
	num_answers = len( sorted_answers )

	for i in range( num_answers ):
		## find first non-empty answer list ##
		if len( sorted_answers[i][4] ) != 0:
			break

	## move all non-empties to the back ##
	sorted_answers = sorted_answers[i:] + sorted_answers[:i]

	## write back to answers.txt ##
	answer_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'w' )
	answer_file.write( '----------------------------------------------------\n')
	answer_file.write( 'i\tj\tA/D\t\t[clue, pattern]\t\t\t\tanswers\n')
	answer_file.write( '----------------------------------------------------\n')
	for line in sorted_answers:
		for item in line:
			answer_file.write( str( item ) + '\t' )
		answer_file.write( '\n' )
		# answer_file.write( str( item ) + '\n' )

	answer_file.close()


def compare_answers( item1, item2 ):
	"""
	Compare function used to sort objects by first answer weight. Returns 1 if item1 is greater
	than item2, 0 if equal, etc.

	@param: {object[]} item1 The first list element
	@param: {object[]} item2 The second list element
	@return: {integer}
	"""
	if ( len( item1[4] ) > len( item2[4] ) ):
		return 1
	elif ( len( item1[4] ) < len( item2[4] ) ):
		return -1
	else:
		return 0


def create_puzzle( puzzle_name, extension ):
	"""
	@param: {string} puzzle_name The path to the file storing the puzzle's structure
	@param: {string} extension Which skeleton file to read from (skeleton, solution, output)
	@return: {string[][]} The puzzle's array representation
	"""
	puzzle_name = clue_scraper.strip_puzzle_name( puzzle_name )
	skeleton_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-' + extension + '.txt', 'r' )
	puzzle_arr = []

	for line in skeleton_file:
		row_arr = []
		for char in line:
			if char == ' ':
				continue
			elif char == '_':
				row_arr.append( ' ' )
			elif char == '0' or char.isalpha(): # note: this actually causes problems with some puzzles (which I have deleted)
				row_arr.append( char )

		puzzle_arr.append( row_arr )

	skeleton_file.close()
	return puzzle_arr


def write_puzzle( puzzle_name, puzzle ):
	"""
	@param: {string} puzzle_name The path to the file storing the puzzle's text representation
	@param: {string[][]} puzzle The puzzle's array representation
	"""
	puzzle_name = clue_scraper.strip_puzzle_name( puzzle_name )
	out_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-output.txt' , 'w' )
	height = len( puzzle )
	width = len( puzzle[0] )

	for i in range( height ):
		for j in range( width ):
			out_file.write( puzzle[i][j] + ' ' )
		out_file.write( '\n' )

	out_file.close()


def print_puzzle( array ):
	"""
	@param: {string[][]} array The puzzle's array representation
	"""
	height = len( array )
	width = len( array[0] )
	print('_' * ( width * 2 - 1 ) )
	for i in range( height ):
		line = ''
		for j in range( width ):
			letter = array[i][j]
			if letter == '0': # black squares
				line += letter
			else:
				if letter.islower(): # wrong answer when evaluating
					line += '\033[90m|\033[91m' + letter.upper()
				else: # correct answer or not evaluating yet
					line += letter
		print( line )

	print( '-' * ( width * 2 - 1 ) )
