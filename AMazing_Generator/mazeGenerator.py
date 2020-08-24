## AUTHOR: JORDAN RANDLEMAN
# python3 mazeGenerator.py

###############################################################################
# A_MAZING GENERATION -:- GET MAZE DIMENSIONS:
###############################################################################

import sys

while True:
	try: # GET USER'S MAZE DIMENSIONS
		SIZE = int(input('\nDimension of Your Maze (greater than 7, ie 25):\n>> ')) 
		if SIZE < 8:
			print("\nInvalid Dimension! Choose 8x8+")
		else:
			break
	except ValueError as err:
		print("\n##########################################################")
		sys.stdout.write("Invalid Input! Only enter a single number > 7 as the")
		print(" \ndimension for your maze (ie 9 would generate a 9x9 maze)")
		print("##########################################################")


###############################################################################
# GLOABAL VAR/ARR DECLARATION
###############################################################################

import random

ESIZE = ((SIZE - 3) // 2) # NUMBER OF (E)DITABLE ROWS
maze = [[0 for height in range(SIZE + 1)] for width in range(SIZE + 1)] #SIZE^2

if SIZE % 2 == 1:
	highMin = (SIZE - 1) // 4
	lowMax = SIZE - highMin
else:
	highMin = SIZE // 4
	lowMax = SIZE - highMin

# max/mins limiting random generation range for 1's (leaves space for 2's)
min1 = random.choice(range(1, highMin))
max1 = random.choice(range(lowMax, SIZE - 1))
min2 = random.choice(range(1, highMin))
max2 = random.choice(range(lowMax, SIZE - 1))

arr1M = [(z*2) for z in range(1, ESIZE + 1)] # Array of 1 column
arr2M = [(z*2) for z in range(1, ESIZE + 1)] # Array of 2 column
arr1N = [0 for z in range(ESIZE + 1)] # Array of 1 rows
arr2N = [0 for z in range(ESIZE + 1)] # Array of 2 rows

for i in range(ESIZE): # randomly generate 1's
	if i % 2 == 0:
		arr1N[i] = random.choice(range(min1, max1))
	else:
		arr1N[i] = random.choice(range(min2, max2))

MS1, NS1 = 0, random.choice(range(1,SIZE - 1)) # start point
MFIN1, NFIN1 = SIZE - 1, arr1N[ESIZE - 1] # end point

for j in range(ESIZE): # randomly generate 2's
	arr2N[j] = random.choice(range(1,SIZE - 1))
	while arr2N[j] in arr1N: # make sure 2 not in range of 1's
		arr2N[j] = random.choice(range(1,SIZE - 1))

# holds last col/row stacked 2 position
twoCol, twoRow = [0 for z in range(ESIZE + 1)], [0 for z in range(ESIZE + 1)]
# holds last col/row 2 position
triCol, triRow = [0 for z in range(ESIZE + 1)], [0 for z in range(ESIZE + 1)]

###############################################################################
# 1 & 2 PATH FILL FUNCTIONS
###############################################################################

def fill_ones(): # insert the randomly generated 1's
	maze[MS1][NS1], maze[MS1 + 1][NS1] = 1, 1
	for i in range(ESIZE):
		maze[arr1M[i]][arr1N[i]], maze[arr1M[i] + 1][arr1N[i]] = 1, 1
	maze[MFIN1][NFIN1] = 1


def fill_twos(): # insert the randomly generated 2's
	for i in range(ESIZE):
		maze[arr2M[i]][arr2N[i]] = 2

###############################################################################
# 1 & 2 PATH CONNECTION FUNCITONS
###############################################################################

def seek_point_connection(from_col, from_row, to_col, to_row, fill_num):
	if to_row < from_row: # fill space between randomly generated 1's in row
		for i in range(to_row, from_row + 1):
			maze[to_col][i] = fill_num
	else:
		for i in range(from_row, to_row + 1):
			maze[to_col][i] = fill_num


def seek_ones(): # fill each row connecting each generated 1 with  more 1's
	seek_point_connection(MS1,NS1,arr1M[0],arr1N[0],1)
	for i in range(ESIZE - 1):
		seek_point_connection(arr1M[i],arr1N[i],arr1M[i + 1],arr1N[i + 1],1)
	seek_point_connection(arr1M[ESIZE - 1],arr1N[ESIZE - 1],MFIN1,NFIN1,1)


def seek_twos():
	for i in range(ESIZE): # fill space btwn randomly generated 2's per row
		if arr2N[i] > arr1N[i]: # if 2 made after 1
			greater = arr2N[i]
			lower = arr1N[i]
		else:
			greater = arr1N[i] # if 1 made after 2
			lower = arr2N[i]
		# fill space with 2's
		while lower < greater:
			maze[arr2M[i]][lower] = 2
			lower += 1
		# figure where end of 2 row was to then generate 2's going down from it
		if arr2N[i] > arr1N[i]:
			twoRow[i] = lower
		else:
			twoRow[i] = arr2N[i]
		twoCol[i] = arr2M[i] + 1
		
		
def fill_two_cols():
	# if space below, R&L of current space is 0 & !border put 2 and move down
	for i in range(ESIZE):
		j = twoCol[i]
		k = twoRow[i]
		while (maze[j+1][k] == 0) and (j != SIZE-2) and (maze[j][k-1] == 0) and (maze[j][k+1] == 0):
			maze[j][k] = 2
			j += 1
		# store column and row of last 2 in column of 2's
		triCol[i] = j
		triRow[i] = k

###############################################################################
# 3 & 4 PATH FILL & CONNECTION FUNCITONS
###############################################################################

def seek_put_threes():
	# put 3's L&R of last 2 from column above valid (ie no #'s or border')
	for i in range(ESIZE):
		j = triRow[i]
		k = triRow[i]
		while is_valid_three(triCol[i], k, 1) == 1: # check left
			maze[triCol[i]][k] = 3 # add 3 left
			k -= 1
		while is_valid_three(triCol[i], j, 2) == 1: # check right
			maze[triCol[i]][j] = 3 # add 3 right
			j += 1


def seek_put_fours():
	for i in range(2,SIZE - 2): # no fours within top/bottom borders
		for j in range(2,SIZE - 2): # no fours within L/R borders
			if maze[i][j] != 0:
				if is_valid_four(i, j, 1) == 1: # check up
					maze[i - 1][j] = 4 # move up
				if is_valid_four(i, j, 2) == 1: # check left
					maze[i][j - 1] = 4 # move left
				if is_valid_four(i, j, 3) == 1: # check down
					maze[i + 1][j] = 4 # move down
				if is_valid_four(i, j, 4) == 1: # check right
					maze[i][j + 1] = 4 # move right
			

def is_valid_three(row, col, direction):
	if direction == 1: # left
		if maze[row][col - 1] == 0 and maze[row + 1][col] == 0:
			if maze[row + 1][col - 1] == 0 and maze[row - 1][col - 1] == 0:
				if (maze[row][col + 1] == 0 or maze[row][col + 1] == 3) and col != 1:
					return 1
		return 0
	elif direction == 2: # right
		if maze[row][col + 1] == 0 and maze[row + 1][col] == 0:
			if maze[row + 1][col + 1] == 0 and maze[row - 1][col + 1] == 0:
				if (maze[row][col - 1] == 0 or maze[row][col - 1] == 3) and col != SIZE - 2:
					return 1
		return 0


def is_valid_four(row, col, move): # checks if a place is valid for being filled by a number
	if move == 1: # up
		if maze[row-1][col] == 0 and maze[row-2][col] == 0 and maze[row-1][col-1] == 0 and maze[row-1][col+1] == 0:
			return 1
	elif move == 2: # left
		if maze[row][col-1] == 0 and maze[row][col-2] == 0 and maze[row-1][col-1] == 0 and maze[row+1][col-1] == 0:
			return 1
	elif move == 3: # down
		if maze[row+1][col] == 0 and maze[row+2][col] == 0 and maze[row+1][col-1] == 0 and maze[row+1][col+1] == 0:
			return 1
	else: # right
		if maze[row][col+1] == 0 and maze[row][col+2] == 0 and maze[row-1][col+1] == 0 and maze[row+1][col+1] == 0:
			return 1
	return 0

###############################################################################
# TAILOR & PRINT MAZE FUNCITON
###############################################################################

def check_even_maze_dimension():
	if SIZE % 2 == 1: # if odd fine - if even need to shift exit under opening
		return
	row = SIZE - 2 # second to last row
	flag = 0 # checks if empty spot found to the R in traversal
	for col in range(SIZE): # find column in last row of the current exit
		if maze[SIZE - 1][col] == 1:
			break
	for j in range(col, SIZE - 1): # traverse second to last row for R opening
		if maze[row][j] != 0:
			flag += 1
			break
	if flag == 0:
		for j in range(1, col): # traverse second to last row for L opening
			if maze[row][j] != 0:
				break
	maze[SIZE - 1][col] = 0 # remove old exit
	maze[SIZE - 1][j] = 1 # add new exit


def print_maze():
	for i in range(SIZE):
		for j in range(SIZE):
			if maze[i][j] != 0:
				maze[i][j] = " " # path/opening
			else:
				maze[i][j] = "\033[7m \033[0m" # wall/blocked
			sys.stdout.write(maze[i][j])
		sys.stdout.write("\n")

###############################################################################
# INIT FUNCTION: FILL MAZE IN 4 SEQUENCES: 1 INITIAL PATH, THEN 3 BRANCHING OFF
###############################################################################

def generate_maze():
	print("\n#########################")
	print("# PYTHON MAZE GENERATOR #")
	print("#########################\n")
	fill_ones() # generate 1's
	fill_twos() # generate 2's outside of 1's 
	seek_ones() # connect 1's
	seek_twos() # connect 2's
	fill_two_cols() # create down columns of 2's from last 2
	seek_put_threes() # create 3's branching to L & R of bottom 2 in col
	seek_put_fours() # create 4's branching top down L R as possible everywhere
	check_even_maze_dimension()
	print_maze()
	print("\n#########################")
	print("#   TOP/DWN = IN/OUT    #")
	print("#########################\n")

generate_maze()
