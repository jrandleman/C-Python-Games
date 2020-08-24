/* AUTHOR: JORDAN RANDLEMAN -:- SUDOKU GAME GENERATOR WITH TXT FILE SAVE-GAME FUNCITONALITY */

/***
 * Compile: $ gcc -std=c99 -o sudokuSavesInC sudokuSavesInC.c
 *          $ ./sudokuSavesInC mySudokuSave.txt
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define M 9

/*
PASS A TEXT FILE AS AN ARGUMENT IN ORDER TO SAVE OR RETRIEVE YOUR CURRENT/
PREVIOUS SUDOKU GAME (ie ./sudokuSavesInC mySudokuSave.txt)
*/

/* FUNCTION DECLARATION */
void playerMove(char [2], int, int);
void makePuzzle(int);
void prepPuzzle(int);
void swapRowColBox();
void swapRowColLoop(int);
void mixCols();
int iOf(int*, int, int);
void printPuzzle();
int checkBoard(int,int,int);
int conditionalBoard(int);
int checkWin();
int checkFileEmpty(char*);
void readFile(char*);
void saveFile(char*);

/* GLOBAL VARS */
int AS[M][M];
int rowArray[6][3], colArray[6][3];
int aRowCol[2][3], bRowCol[2][3], cRowCol[2][3];

/******************************************************************************/
/* MAIN FUNCTION */
/******************************************************************************/

int main(int argc, char *argv[]) { /* ALLOWS USER TO PASS A SAVE GAME TXT FILE ARG */
	int newGame = 2, check, uCol, uNum;
	char uRow[2];
	if(argc == 2) { /* IF FILE NAME PASSED AS ARG */
		if(checkFileEmpty(argv[1]) == 0) { /* IF FILE NOT EMPTY */
			while(1) { /* CONTINUED OR NEW GAME? */
				printf("\n\033[1mContinue Game (enter 1 for yes, 2 for new game, 0 to exit)?\033[0m\n>> ");
				scanf("%d", &newGame);
				if(newGame > 2)
					printf("\n\033[1m\033[31mERROR:\033[0m\033[1m Invalid input!\033[0m\n>> Enter 1 to continue your game, 2 to start anew, or 0 to exit!\n");
				else break;
			}
			if(newGame == 1)
				readFile(argv[1]);
			else if(newGame == 0)
				return 0;
		}
	}
	if(argc == 1 || newGame == 2) { /* IF NO FILE ARG OR CHOSE NEW GAME */
		printf("\nPreferred Difficulty?\n1 ------- EASY\n2 ----- MEDIUM\n3 ------- HARD\n0 ------- EXIT\nNUMBER >> ");
		scanf("%d",&check);
		if(check == 0) return 0;
		if(!(check >= 1 && check <= 3)) {
			printf("\n\033[1m\033[31mERROR:\033[0m\033[1m Invalid input!\033[0m\n>> Enter 1, 2, or 3 for the associated difficulty.");
			return 0;
		}
		makePuzzle(check);
	}
	while(1) { /* GET PLAYER MOVE UNTIL QUITS */
		printf("\nEdit which cell? (0 = space)\nLETTER=ROW -:- NUMBER=COLUMN");
		printf("\n => ENTER 0 TO EXIT\n");
		printf("ROW: ");
		scanf("%s", uRow);
		if(uRow[0] == '0') {
			if(argc == 2) saveFile(argv[1]);
			return 0;
		} else if(!((uRow[0] >= 'A' && uRow[0] <= 'I')||(uRow[0] >= 'a' && uRow[0] <= 'i'))) {
			printf("\n\033[1m\033[31mERROR:\033[0m\033[1m Invalid input!\033[0m\n>> Enter a letter 'A'-'I' to choose a row.\n");
			continue;
		}
		printf("COLUMN: ");
		scanf("%d", &uCol);
		if(uCol == 0) {
			if(argc == 2) saveFile(argv[1]);
			return 0;
		} else if(uCol < 1 || uCol > 9) {
			printf("\n\033[1m\033[31mERROR:\033[0m\033[1m Invalid input!\033[0m\n>> Enter a Number 1-9 to choose a column.\n");
			continue;
		}
		printf("New Number: ");
		scanf("%d", &uNum);
		if(uNum == 0) {
			if(argc == 2) saveFile(argv[1]);
			return 0;
		}
		playerMove(uRow, uCol, uNum);
		printPuzzle();
		if(checkWin() == 1) {
			printf("\n\033[1m/*******************************/\n");
			printf("/*       !!! WINNER !!!        */\n");
			printf("/*******************************/\033[0m\n");
			return 0;
		}
	}
}

/******************************************************************************/
/* FILE FUNCTIONS */
/******************************************************************************/

int checkFileEmpty(char *name) {
	FILE *fp;
	if(( fp = fopen(name, "r")) == NULL) return 1;
	fclose(fp);
	return 0;
}

void readFile(char *name) {
	FILE *fp;
	int num, *p = &AS[0][0];
	if((fp = fopen(name, "r")) == NULL) return;
	while(fscanf(fp, "%d", &num) == 1) *p ++ = num;
	fclose(fp);
	printf("\n\033[1m/*******************************/\n");
	printf("/*        SUDOKU IN C!         */\n");
	printf("/*******************************/\033[0m\n");
	printPuzzle();
}

void saveFile(char *name) {
	int choice;
	while(1) {
		printf("\n\033[1mSave your current game (enter 1 for yes, 0 for no)?\033[0m\n>> ");
		scanf("%d",&choice);
		if(choice == 0)
			return;
		else if (choice == 1)
			break;
		else
			printf("\n\033[1m\033[31mERROR:\033[0m\033[1m Invalid input!\033[0m\n>> Enter 1 to save and quit your current game, or 2 to quit without saving.\n");
	}
	FILE *fp;
	if((fp = fopen(name, "w")) == NULL) return;
	for(int *p = &AS[0][0]; p <= &AS[8][8]; p++) fprintf(fp, "%d\n", *p);
	fclose(fp);
}

/******************************************************************************/
/* PLAYER MOVE */
/******************************************************************************/

void playerMove(char row[2], int col, int n) {
	int r, c = col - 1, valid, i, j;
	r = row[0] - 'A';
	if(row[0] >= 'a' && row[0] <= 'z') r -= 32; // convert to lowercase

	valid = checkBoard(r,c,n);
	if(AS[r][c] != 0 || valid < 3) {
		printf("\n\033[1m/*******************************/\n");
		if(AS[r][c] != 0)
			printf("/*     NOT AN EMPTY SPACE!     */");
		else if(valid == 0)
			printf("/*      %d ALREADY IN ROW!      */", n);
		else if(valid == 1)
			printf("/*    %d ALREADY IN COLUMN!     */", n);
		else if(valid == 2)
			printf("/*      %d ALREADY IN BOX!      */", n);
		printf("\n/*******************************/\033[0m\n");
	} else
		AS[r][c] = n;
}

/******************************************************************************/
/* CHECK BOARD FOR NUMBER IN ROW, COLUMN, AND BOX */
/******************************************************************************/

int checkBoard(int r, int c, int n) {
	int i, br, bc, j;
	/* CHECK ROW */
	for(i = 0; i < M; i++) if(AS[r][i] == n) return 0;
	/* CHECK COLUMN */
	for(i = 0; i < M; i++) if(AS[i][c] == n) return 1;
	/* CHECK WHICH BOX ROW */
	br = conditionalBoard(r);
	/* CHECK WHICH BOX COLUMN */
	bc = conditionalBoard(c);
	for(i = br; i < br + 3; i++) for(j = bc; j < bc + 3; j++) if(AS[i][j] == n) return 2;
	return 3;
}

int conditionalBoard(int n) {
	if(n >= 0 && n <= 2)
		return 0;
	else if (n >= 3 && n <= 5)
		return 3;
	else
		return 6;
}

/******************************************************************************/
/* CHECK IF PLAYER WINNER FUNCTION */
/******************************************************************************/

int checkWin() {
	for(int *p = &AS[0][0]; p <= &AS[8][8]; p++) if(*p == 0) return 0;
	return 1;
}

/******************************************************************************/
/* INIT SUDOKU BOARD */
/******************************************************************************/

void makePuzzle(int flag) {
	int l, i, j, k, tempAn, tempBn, tempCn, tempAr[M], tempBr[M], tempCr[M];
	/* GENERATE BOARD */
	int x1[M] = {1,2,3,4,5,6,7,8,9}, x2[M] = {4,5,6,7,8,9,1,2,3};
	int x3[M] = {7,8,9,1,2,3,4,5,6}, x4[M] = {2,3,1,5,6,4,8,9,7};
	int x5[M] = {5,6,4,8,9,7,2,3,1}, x6[M] = {8,9,7,2,3,1,5,6,4};
	int x7[M] = {3,1,2,6,4,5,9,7,8}, x8[M] = {6,4,5,9,7,8,3,1,2};
	int x9[M] = {9,7,8,3,1,2,6,4,5};
	for(i = 0; i < M; i++) {
		AS[0][i] = x1[i];
		AS[1][i] = x2[i];
		AS[2][i] = x3[i];
		AS[3][i] = x4[i];
		AS[4][i] = x5[i];
		AS[5][i] = x6[i];
		AS[6][i] = x7[i];
		AS[7][i] = x8[i];
		AS[8][i] = x9[i];
	}

	mixCols();
	srand((int)time(NULL));
	/* SWAP NUMBERS */
	int switchNums = rand()%3 + 2, ranSize = switchNums*2;
	int ranFlips[ranSize];
	i = 0;
	while(i < ranSize) {
		int switchKey = rand()%9 + 1;
		if(iOf(ranFlips,i,switchKey) == -1) ranFlips[i++] = switchKey;
	}
	for(l = 0; l < ranSize; l+=2)
		for( i = 0; i < M; i++)
			for(j = 0; j < M; j++) {
				if(AS[i][j] == ranFlips[l])
					AS[i][j] = ranFlips[l+1];
				else if(AS[i][j] == ranFlips[l+1])
					AS[i][j] = ranFlips[l];
			}
	/* GENERATE RANDOM ROW/COL IDXS TO SWITCH WITH ONE ANOTHER IN AS */
	swapRowColBox();
	int rowA1[3], rowA2[3], rowB1[3], rowB2[3], rowC1[3], rowC2[3];
	int colA1[3], colA2[3], colB1[3], colB2[3], colC1[3], colC2[3];
	for(i = 0; i < 3; i ++) {
		rowA1[i] = rowArray[0][i];
		rowA2[i] = rowArray[1][i];
		rowB1[i] = rowArray[2][i];
		rowB2[i] = rowArray[3][i];
		rowC1[i] = rowArray[4][i];
		rowC2[i] = rowArray[5][i];
		colA1[i] = colArray[0][i];
		colA2[i] = colArray[1][i];
		colB1[i] = colArray[2][i];
		colB2[i] = colArray[3][i];
		colC1[i] = colArray[4][i];
		colC2[i] = colArray[5][i];
	}
	/* SWAP ROWS */
	for(k = 0; k < 3; k++)
		for(i = 0; i < M; i++) {
			tempAr[i] = AS[rowA1[k]][i];
			AS[rowA1[k]][i] = AS[rowA2[k]][i];
			AS[rowA2[k]][i] = tempAr[i];

			tempBr[i] = AS[rowB1[k]][i];
			AS[rowB1[k]][i] = AS[rowB2[k]][i];
			AS[rowB2[k]][i] = tempBr[i];

			tempCr[i] = AS[rowC1[k]][i];
			AS[rowC1[k]][i] = AS[rowC2[k]][i];
			AS[rowC2[k]][i] = tempCr[i];
		}
	/* SWAP COLUMNS */
	for(k = 0; k < 3; k++)
		for(l = 0; l < M; l++) {
			tempAn = AS[l][colA1[k]];
			AS[l][colA1[k]] = AS[l][colA2[k]];
			AS[l][colA2[k]] = tempAn;

			tempBn = AS[l][colB1[k]];
			AS[l][colB1[k]] = AS[l][colB2[k]];
			AS[l][colB2[k]] = tempBn;

			tempCn = AS[l][colC1[k]];
			AS[l][colC1[k]] = AS[l][colC2[k]];
			AS[l][colC2[k]] = tempCn;
		}
	/* ROTATE PUZZLE WITH 33% CHANCE TO EXECUTE */
	int rotatedPuzzle[M][M], rotateKey = rand()%3 + 1;
	if(rotateKey == 2) {
		for(j = 0; j < M; j++) for(k = 0; k < M; k++) rotatedPuzzle[j][k] = AS[k][j];
		for(j = 0; j < M; j++) for(k = 0; k < M; k++) AS[j][k] = rotatedPuzzle[j][k];
	}
	/* INSERT RANDOM SPACES => REPRESENTED BY "0's"*/
	prepPuzzle(flag);
	/* PRINT INITIAL HEADER AND THE BOARD */
	printf("\n\033[1m/*******************************/\n");
	printf("/*        SUDOKU IN C!         */\n");
	printf("/*******************************/\033[0m\n");
	printPuzzle();
}

/******************************************************************************/
/* PRINT FUNCTION */
/******************************************************************************/

void printPuzzle() {
	int i, j;
	char letters[M] = "ABCDEFGHI", *s = letters;
	printf("\n    1 2 3   4 5 6   7 8 9  \n");
	printf("  +-----------------------+\n");
	for(i = 0; i < M; i++, s++) { /* print rows */
		printf("%c | ", *s);
		for(j = 0; j < M; j++) { /* print cols */
			printf("%d ", AS[i][j]);
			if(j == 2 || j == 5) printf("| ");
		}
		printf("|\n");
		if(i == 2 || i == 5) printf("  |-----------------------|\n");
	}
	printf("  +-----------------------+\n");
}

/******************************************************************************/
/* INDEXOF FUNCTION */
/******************************************************************************/

int iOf(int *p, int size, int num) {
	int idx;
	for(idx = 0; idx < size; idx++, p++) if(*p == num) return idx;
	return -1;
}

/******************************************************************************/
/* EMPTY SPACE GENERATION/INSERTION FUNCTION */
/******************************************************************************/

void prepPuzzle(int flag) {
	srand((int)time(NULL));
	/* ALTERS SPACE-CELL SPREAD AS PER DIFFICULTY OPTION */
	int spNum1, spNum2, spNum3;
	spNum1 = flag + 2;
	spNum2 = flag + 3;
	(flag < 3) ? (spNum3 = flag + 4) : (spNum3 = 6);
	int ASpace[M][6], i, j, k, ranNumber, counter, size, limit;
	for(j = 0; j < M; j++) {
		if ((j == 4 || j == 7) || j == 0)
			limit = spNum1;
		else if ((j == 1 || j == 3) || (j == 8))
			limit = spNum2;
		else
			limit = spNum3;
		counter = 0;
		while(counter < limit) {
			ranNumber = rand()%9;
			if(iOf(ASpace[j],6,ranNumber) == -1) ASpace[j][counter++] = ranNumber;
		}
		for(k = limit; k < 6; k++) ASpace[j][k] = 0;
	}
	for( i = 0; i < M; i++) {
		if((i == 4 || i == 7) || i == 0)
			size = spNum1;
		else if((i == 1 || i == 3) || (i == 8))
			size = spNum2;
		else
			size = spNum3;
		for(k = 0; k < size; k++) AS[i][ASpace[i][k]] = 0;
	}
}

/******************************************************************************/
/* SCRAMBLING FUNCTIONS */
/******************************************************************************/

void swapRowColBox() {
	int j;
	swapRowColLoop(0);
	swapRowColLoop(1);
	swapRowColLoop(2);
	for(j = 0; j < 3; j++) {
		rowArray[0][j] = aRowCol[0][j];
		rowArray[1][j] = aRowCol[1][j];
		rowArray[2][j] = bRowCol[0][j];
		rowArray[3][j] = bRowCol[1][j];
		rowArray[4][j] = cRowCol[0][j];
		rowArray[5][j] = cRowCol[1][j];
		colArray[0][j] = aRowCol[0][j];
		colArray[1][j] = aRowCol[1][j];
		colArray[2][j] = bRowCol[0][j];
		colArray[3][j] = bRowCol[1][j];
		colArray[4][j] = cRowCol[0][j];
		colArray[5][j] = cRowCol[1][j];
	}
}

void swapRowColLoop(int letterArr) {
	srand((int)time(NULL));
	int size = 0, i, j, *p, *q, temp, ranNum, arr1[3], arr2[3];
	while(size < 3) {
		ranNum = rand()%3;
		if(iOf(arr1,size,ranNum) == -1) arr1[size++] = ranNum;
	}
	size = 0;
	while(size < 3) {
		ranNum = rand()%3;
		if(iOf(arr2,size,ranNum) == -1) arr2[size++] = ranNum;
	}
	for(i = 0; i < 3; i++) {
		if(arr1[i] == arr2[i]) {
			temp = arr1[i];
			if(i != 2)
				arr1[i] = arr1[i+1], arr1[i+1] = temp;
			else
				arr1[i] = arr1[i-1], arr1[i-1] = temp;
		}
	}
	if(letterArr == 0)
		p = &aRowCol[0][0];
	else if(letterArr == 1)
		p = &bRowCol[0][0];
	else
		p = &cRowCol[0][0];
	for(j = 0; j < 2; j++) {
		(j == 0) ? (q = &arr1[0]) : (q = &arr2[0]);
		for(i = 0; i < 3; i++, q++, p++) *p = *q;
	}
}

void mixCols() {
	srand((int)time(NULL));
	int p, temp, temp1, temp2, rn;
	rn = rand()%12 + 1;
	for(p = 0; p < M; p++) {
		if((rn == 1 || rn == 2) || (rn == 3 || rn == 4)) {
			temp = AS[p][0];
			AS[p][0] = AS[p][3];
			AS[p][3] = AS[p][6];
			AS[p][6] = temp;
			if(rn == 1) {
				temp1 = AS[p][8];
				AS[p][8] = AS[p][5];
				AS[p][5] = AS[p][2];
				AS[p][2] = temp1;
			} else {
				temp1 = AS[p][7];
				AS[p][7] = AS[p][4];
				AS[p][4] = AS[p][1];
				AS[p][1] = temp1;
				if(rn == 3 || rn == 4) {
					if(rn == 3) {
						temp2 = AS[p][8];
						AS[p][8] = AS[p][5];
						AS[p][5] = AS[p][2];
						AS[p][2] = temp2;
					} else {
						temp2 = AS[p][2];
						AS[p][2] = AS[p][5];
						AS[p][5] = AS[p][8];
						AS[p][8] = temp2;
					}
				}
			}
		} else if((rn == 5 || rn == 6) || (rn == 7 || rn == 8)) {
			temp = AS[p][6];
			AS[p][6] = AS[p][3];
			AS[p][3] = AS[p][0];
			AS[p][0] = temp;
			if(rn == 5) {
				temp1 = AS[p][2];
				AS[p][2] = AS[p][5];
				AS[p][5] = AS[p][8];
				AS[p][8] = temp1;
			} else {
				temp1 = AS[p][1];
				AS[p][1] = AS[p][4];
				AS[p][4] = AS[p][7];
				AS[p][7] = temp1;
				if(rn == 7 || rn == 8) {
					if(rn == 7) {
						temp2 = AS[p][8];
						AS[p][8] = AS[p][5];
						AS[p][5] = AS[p][2];
						AS[p][2] = temp2;
					} else {
						temp2 = AS[p][2];
						AS[p][2] = AS[p][5];
						AS[p][5] = AS[p][8];
						AS[p][8] = temp2;
					}
				}
			}
		} else if(rn == 9 || rn == 10) {
			temp = AS[p][7];
			AS[p][7] = AS[p][4];
			AS[p][4] = AS[p][1];
			AS[p][1] = temp;
			temp1 = AS[p][2];
			AS[p][2] = AS[p][5];
			AS[p][5] = AS[p][8];
			AS[p][8] = temp1;
			if(rn == 10) {
				temp2 = AS[p][6];
				AS[p][6] = AS[p][3];
				AS[p][3] = AS[p][0];
				AS[p][0] = temp2;
			}
		} else if(rn == 11 || rn == 12) {
			temp = AS[p][1];
			AS[p][1] = AS[p][4];
			AS[p][4] = AS[p][7];
			AS[p][7] = temp;
			temp1 = AS[p][8];
			AS[p][8] = AS[p][5];
			AS[p][5] = AS[p][2];
			AS[p][2] = temp1;
			if(rn == 12) {
				temp2 = AS[p][0];
				AS[p][0] = AS[p][3];
				AS[p][3] = AS[p][6];
				AS[p][6] = temp2;
			}
		}
	}
}
