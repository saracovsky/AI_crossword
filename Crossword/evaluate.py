
import clue_scraper
import puzzle_structure

def compare_results( puzzle_name ):
	"""
	Compares [puzzle_name]-solutions.txt with [puzzle_name]-output.txt

	@param: {String} puzzle_name
	@return: {String[][]} The array representing differences between actual and expected answers
	"""
	## get our answers and actual solution ##
	our_arr = puzzle_structure.create_puzzle( puzzle_name, 'output' )
	solution_arr = puzzle_structure.create_puzzle( puzzle_name, 'solution' )
	diff_arr = puzzle_structure.create_puzzle( puzzle_name, 'skeleton' )

	height = len( our_arr )
	width = len( our_arr[0] )

	## compare each character ##
	for i in range( height ):
		for j in range( width ):
			if our_arr[i][j] == solution_arr[i][j]:
				diff_arr[i][j] = our_arr[i][j]
			else:
				diff_arr[i][j] = our_arr[i][j].lower()

	## return the puzzle with differences highlighted for analysis ##
	write_diff( puzzle_name, diff_arr )
	return diff_arr


def write_diff( puzzle_name, diff_arr ):
	"""
	Write the difference in our solution and the actual solution to the diff file

	@param: {String} puzzle_name
	@param: {String[][]} The array representing differences between actual and expected answers
	"""
	puzzle_name = clue_scraper.strip_puzzle_name( puzzle_name )
	out_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-diff.txt' , 'w' )

	height = len( diff_arr )
	width = len( diff_arr[0] )
	diff_string = ''

	for i in range( height ):
		for j in range( width ):
			diff_string += diff_arr[i][j]

	out_file.write( diff_string )
	out_file.close()


def score_puzzle( diff_arr ):
	"""
	Evaluate the puzzle based on the differences between our solution and the correct solution.
	One point for each correct letter, plus 10 points for each fully correct word.

	@param: {string[][]} diff_arr The puzzle with differences highlighted
	@return: {float, float} Percent of squares correct, percent of words correct
	"""
	## count the wrong letters ##
	height = len( diff_arr )
	width = len( diff_arr[0] )
	total_letters = 0
	wrong_letters = 0
	total_answers = 0
	correct_answers = 0

	for i in range( height ):
		for j in range( width ):
			if ( diff_arr[i][j] ) != '0':
				total_letters += 1

			## see if word is correct ##
			k, l = i, j
			if ( k == 0 and diff_arr[k][l] != '0' ) or ( diff_arr[k-1][l] == '0' and diff_arr[k][l] != '0' ): # start of a 'down' clue
				total_answers += 1
				while ( True ):
					if diff_arr[k][l].islower():
						break
					if ( k + 1 ) == height or diff_arr[k][l] == '0': # whole answer is correct
						correct_answers += 1
						break
					k += 1

			k, l = i, j
			if ( l == 0 and diff_arr[k][l] != '0' ) or ( diff_arr[k][l-1] == '0' and diff_arr[k][l] != '0' ): # start of an 'across' clue
				total_answers += 1
				while ( True ):
					if diff_arr[k][l].islower():
						break
					if ( l + 1 ) == width or diff_arr[k][l] == '0': # whole answer is correct
						correct_answers += 1
						break
					l += 1

			## see if letter is correct ##
			if diff_arr[i][j].islower():
				wrong_letters += 1

	## print puzzle with wrong letters highlighted ##
	print( chr(27) )
	puzzle_structure.print_puzzle( diff_arr )

	## print some statistics ##
	print( str( total_letters - wrong_letters ) + ' squares correct out of ' + str( total_letters ) )
	print( str( correct_answers ) + ' answers correct out of ' + str( total_answers ) )
	print( 'score: ' +  str( ( total_letters - wrong_letters ) + 10 * total_answers ) )

	letters_correct = 100 * ( float ( total_letters - wrong_letters ) / total_letters )
	words_correct = 100 * ( float( correct_answers ) / total_answers )
	return letters_correct, words_correct
