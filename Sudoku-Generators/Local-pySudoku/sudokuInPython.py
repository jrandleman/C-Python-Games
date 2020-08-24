# AUTHOR: JORDAN RANDLEMAN

import random
AS = [[],[],[],[],[],[],[],[],[]]
rowArray, colArray = [[],[],[],[],[],[]], [[],[],[],[],[],[]]

###############################################################################
# PRINT FUNCTION
###############################################################################

def printPuzzle():
	letters = ["A","B","C","D","E","F","G","H","I"]
	print("\n    1 2 3   4 5 6   7 8 9  ")
	print("  +-----------------------+")
	for i in range(9):
		print("{} | ".format(letters[i]), end = "")
		for j in range(9):
			print("{} ".format(AS[i][j]), end = "")
			if j == 2 or j == 5:
				print("| ", end = "")
		print("|")
		if i == 2 or i == 5:
			print("  |-----------------------|")
	print("  +-----------------------+")
	return

###############################################################################
# CHECK IF PLAYER WINNER FUNCTION
###############################################################################

def checkWin():
	for i in range(9):
		for j in range(9):
			if AS[i][j] == 0:
				return 0
	return 1

###############################################################################
# CHECK BOARD FOR NUMBER IN ROW, COLUMN, AND BOX
###############################################################################

def checkBoard(r, c, n):
	# CHECK ROW
	for i in range(9):
		if AS[r][i] == n:
			return 0
	# CHECK COLUMN
	for i in range(9):
		if AS[i][c] == n:
			return 1
	# CHECK WHICH BOX ROW
	br = conditionalBoard(r)
	# CHECK WHICH BOX COLUMN
	bc = conditionalBoard(c)
	i = br
	while i < br + 3:
		j = bc
		while j < bc + 3:
			if AS[i][j] == n:
				return 2
			j += 1
		i += 1
	return 3

def conditionalBoard(n):
	if n >= 0 and n <= 2:
		return 0
	elif n >= 3 and n <= 5:
		return 3
	else:
		return 6

###############################################################################
# PLAYER MOVE
###############################################################################

def playerMove(row, col, n):
	c = col - 1
	if row == 'a' or row == 'A':
		r = 0
	elif row == 'b' or row == 'B':
		r = 1
	elif row == 'c' or row == 'C':
		r = 2
	elif row == 'd' or row == 'D':
		r = 3
	elif row == 'e' or row == 'E':
		r = 4
	elif row == 'f' or row == 'F':
		r = 5
	elif row == 'g' or row == 'G':
		r = 6
	elif row == 'h' or row == 'H':
		r = 7
	elif row == 'i' or row == 'I':
		r = 8
	valid = checkBoard(r,c,n)
	if AS[r][c] != 0 or valid < 3:
		print("\n#################################")
		if AS[r][c] != 0:
			print("#      NOT AN EMPTY SPACE!      #")
		elif valid == 0:
			print("#       {} ALREADY IN ROW!       #".format(n))
		elif valid == 1:
			print("#     {} ALREADY IN COLUMN!      #".format(n))
		elif valid == 2:
			print("#       {} ALREADY IN BOX!       #".format(n))
		print("#################################\n")
	else:
		AS[r][c] = n

###############################################################################
# EMPTY SPACE GENERATION/INSERTION FUNCTION
###############################################################################

def prepPuzzle(flag):
	spNum1 = flag + 2
	spNum2 = flag + 3
	if flag < 3:
		spNum3 = flag + 4
	else:
		spNum3 = 6
	ASpace = [[],[],[],[],[],[],[],[],[]]
	for i in range(9):
		if i == 4 or i == 7 or i == 0:
			num = spNum1
		elif i == 1 or i == 3 or i == 8:
			num = spNum2
		else:
			num = spNum3
		while len(ASpace[i]) < num:
			ranNumber = random.choice(range(9))
			if ranNumber not in ASpace[i]:
				ASpace[i].append(ranNumber)
	for j in range(9):
		for k in range(len(ASpace[j])):
			AS[j][ASpace[j][k]] = 0
	return

###############################################################################
# SCRAMBLING FUNCTIONS
###############################################################################

def swapRowColBox():
	aRowCol = swapRowColLoop()
	bRowCol = swapRowColLoop()
	cRowCol = swapRowColLoop()
	for j in range(3):
		rowArray[0].append(aRowCol[0][j])
		rowArray[1].append(aRowCol[1][j])
		rowArray[2].append(bRowCol[0][j])
		rowArray[3].append(bRowCol[1][j])
		rowArray[4].append(cRowCol[0][j])
		rowArray[5].append(cRowCol[1][j])
		colArray[0].append(aRowCol[0][j])
		colArray[1].append(aRowCol[1][j])
		colArray[2].append(bRowCol[0][j])
		colArray[3].append(bRowCol[1][j])
		colArray[4].append(cRowCol[0][j])
		colArray[5].append(cRowCol[1][j])
	return

def swapRowColLoop():
	arr1, arr2 = [], []
	while len(arr1) < 3:
		ranNum = random.choice(range(3))
		if ranNum not in arr1:
			arr1.append(ranNum)
	while len(arr2) < 3:
		ranNum = random.choice(range(3))
		if ranNum not in arr2:
			arr2.append(ranNum)
	for i in range(3):
		if arr1[i] == arr2[i]:
			if i != 2:
				temp = arr1[i]
				arr1[i] = arr1[i+1]
				arr1[i+1] = temp
			else:
				temp = arr1[i]
				arr1[i] = arr1[i-1]
				arr1[i-1] = temp
	return [arr1,arr2]

def mixCols():
	rn = random.choice(range(1,13))
	for p in range(9):
		if rn == 1 or rn == 2 or rn == 3 or rn == 4:
			temp = AS[p][0]
			AS[p][0] = AS[p][3]
			AS[p][3] = AS[p][6]
			AS[p][6] = temp
			if rn == 1:
				temp1 = AS[p][8]
				AS[p][8] = AS[p][5]
				AS[p][5] = AS[p][2]
				AS[p][2] = temp1
			else:
				temp1 = AS[p][7]
				AS[p][7] = AS[p][4]
				AS[p][4] = AS[p][1]
				AS[p][1] = temp1
				if rn == 3 or rn == 4:
					if rn == 3:
						temp2 = AS[p][8]
						AS[p][8] = AS[p][5]
						AS[p][5] = AS[p][2]
						AS[p][2] = temp2
					else:
						temp2 = AS[p][2]
						AS[p][2] = AS[p][5]
						AS[p][5] = AS[p][8]
						AS[p][8] = temp2
		elif rn == 5 or rn == 6 or rn == 7 or rn == 8:
			temp = AS[p][6]
			AS[p][6] = AS[p][3]
			AS[p][3] = AS[p][0]
			AS[p][0] = temp
			if rn == 5:
				temp1 = AS[p][2]
				AS[p][2] = AS[p][5]
				AS[p][5] = AS[p][8]
				AS[p][8] = temp1
			else:
				temp1 = AS[p][1]
				AS[p][1] = AS[p][4]
				AS[p][4] = AS[p][7]
				AS[p][7] = temp1
				if rn == 7 or rn == 8:
					if rn == 7:
						temp2 = AS[p][8]
						AS[p][8] = AS[p][5]
						AS[p][5] = AS[p][2]
						AS[p][2] = temp2
					else:
						temp2 = AS[p][2]
						AS[p][2] = AS[p][5]
						AS[p][5] = AS[p][8]
						AS[p][8] = temp2
		elif rn == 9 or rn == 10:
			temp = AS[p][7]
			AS[p][7] = AS[p][4]
			AS[p][4] = AS[p][1]
			AS[p][1] = temp
			temp1 = AS[p][2]
			AS[p][2] = AS[p][5]
			AS[p][5] = AS[p][8]
			AS[p][8] = temp1
			if rn == 10:
				temp2 = AS[p][6]
				AS[p][6] = AS[p][3]
				AS[p][3] = AS[p][0]
				AS[p][0] = temp2
		elif rn == 11 or rn == 12:
			temp = AS[p][1]
			AS[p][1] = AS[p][4]
			AS[p][4] = AS[p][7]
			AS[p][7] = temp
			temp1 = AS[p][8]
			AS[p][8] = AS[p][5]
			AS[p][5] = AS[p][2]
			AS[p][2] = temp1
			if rn == 12:
				temp2 = AS[p][0]
				AS[p][0] = AS[p][3]
				AS[p][3] = AS[p][6]
				AS[p][6] = temp2
	return

###############################################################################
# INIT SUDOKU BOARD
###############################################################################

def makePuzzle(flag):
	AS[0] = [1,2,3,4,5,6,7,8,9]
	AS[1] = [4,5,6,7,8,9,1,2,3]
	AS[2] = [7,8,9,1,2,3,4,5,6]
	AS[3] = [2,3,1,5,6,4,8,9,7]
	AS[4] = [5,6,4,8,9,7,2,3,1]
	AS[5] = [8,9,7,2,3,1,5,6,4]
	AS[6] = [3,1,2,6,4,5,9,7,8]
	AS[7] = [6,4,5,9,7,8,3,1,2]
	AS[8] = [9,7,8,3,1,2,6,4,5]
	mixCols()
	ranFlips = []
	switchNums = random.choice(range(2,5))
	ranSize = switchNums*2
	while len(ranFlips) < ranSize:
		switchKey = random.choice(range(1,10))
		if switchKey not in ranFlips:
			ranFlips.append(switchKey)
	l = 0
	while l < ranSize:
		for i in range(9):
			for j in range(9):
				if AS[i][j] == ranFlips[l]:
					AS[i][j] = ranFlips[l+1]
				elif AS[i][j] == ranFlips[l+1]:
					AS[i][j] = ranFlips[l]
		l += 2
	# GENERATE RANDOM ROW/COL IDXS TO SWITCH WITH ONE ANOTHER IN AS
	swapRowColBox()
	rowA1, rowA2, colA1, colA2 = [], [], [], []
	rowB1, rowB2, colB1, colB2 = [], [], [], []
	rowC1, rowC2, colC1, colC2 = [], [], [], []
	for i in range(3):
		rowA1.append(rowArray[0][i])
		rowA2.append(rowArray[1][i])
		rowB1.append(rowArray[2][i])
		rowB2.append(rowArray[3][i])
		rowC1.append(rowArray[4][i])
		rowC2.append(rowArray[5][i])
		colA1.append(colArray[0][i])
		colA2.append(colArray[1][i])
		colB1.append(colArray[2][i])
		colB2.append(colArray[3][i])
		colC1.append(colArray[4][i])
		colC2.append(colArray[5][i])
	# SWAP ROWS
	for k in range(3):
		tempA = AS[rowA1[k]]
		AS[rowA1[k]] = AS[rowA2[k]]
		AS[rowA2[k]] = tempA
		tempB = AS[rowB1[k]]
		AS[rowB1[k]] = AS[rowB2[k]]
		AS[rowB2[k]] = tempB
		tempC = AS[rowC1[k]]
		AS[rowC1[k]] = AS[rowC2[k]]
		AS[rowC2[k]] = tempC
	for k in range(3):
		for l in range(9):
			tempA = AS[l][colA1[k]]
			AS[l][colA1[k]] = AS[l][colA2[k]]
			AS[l][colA2[k]] = tempA
			tempB = AS[l][colB1[k]]
			AS[l][colB1[k]] = AS[l][colB2[k]]
			AS[l][colB2[k]] = tempB
			tempC = AS[l][colC1[k]]
			AS[l][colC1[k]] = AS[l][colC2[k]]
			AS[l][colC2[k]] = tempC
	# ROTATE PUZZLE 33% CHANCE
	rotatedPuzzle = [[],[],[],[],[],[],[],[],[]]
	rotateKey = random.choice(range(1,4))
	if rotateKey == 2:
		for j in range(9):
			for k in range(9):
				rotatedPuzzle[j].append(AS[k][j])
		for j in range(9):
			for k in range(9):
				AS[j][k] = rotatedPuzzle[j][k]
	prepPuzzle(flag)
	printPuzzle()
	return

###############################################################################
# MAIN FUNCTION
###############################################################################

key = 1
while key == 1:
	print("\nPreferred Difficulty?\n1 ----- EASY\n2 --- MEDIUM\n3 ----- HARD\n0 ----- EXIT")
	check = int(input("NUMBER >> "))
	if check == 0:
		break
	elif check not in range(1,4):
		print("\nInvalid input!\nEnter 1, 2, or 3 for the associated difficulty.")
		break
	print("\n#################################")
	print("#       SUDOKU IN PYTHON!       #")
	print("#################################")
	makePuzzle(check)
	while True:
		capLetters = ["A","B","C","D","E","F","G","H","I"]
		lowLetters = ["a","b","c","d","e","f","g","h","i"]
		print("Edit which cell? (0 = space)\nLETTER=ROW -:- NUMBER=COLUMN")
		print(" => ENTER 0 TO EXIT")
		uRow = input("ROW: ")
		if uRow == '0':
			key = 0
			break
		elif uRow not in capLetters and uRow not in lowLetters:
			print("\nInvalid input!\nEnter a letter 'A'-'I' to choose a row.\n")
			continue
		uCol = int(input("COLUMN: "))
		if uCol == 0:
			key = 0
			break
		uNum = int(input("New Number: "))
		if uNum == 0:
			key = 0
			break
		playerMove(uRow, uCol, uNum)
		printPuzzle()
		if checkWin() == 1:
			print("\n#################################")
			print("#         !!! WINNER !!!        #")
			print("#################################")
			key = 0
			break
