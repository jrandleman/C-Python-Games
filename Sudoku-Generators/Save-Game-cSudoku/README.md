# Save-Game-cSudoku
Sudoku Puzzle Generator With Save-Game Functionality! _(played in terminal)_
---------------------------------------------------------------------------------------

Savable puzzle progress when exiting via a text file argument passed in post-compilation execution 
```c
gcc -std=C99 -o sudokuInC sudokuInC.c
./sudokuInC mySave.txt
```

Alternatively, sudoku puzzles can still be played locally by either not passing a text file argument or choosing to play a new game at the start

### Sample Medium Difficulty Sudoku:
```
/*******************************/
/*        SUDOKU IN C!         */
/*******************************/

    1 2 3   4 5 6   7 8 9  
  +-----------------------+
A | 8 7 0 | 0 5 0 | 0 2 4 |
B | 6 4 0 | 0 0 0 | 3 0 9 |
C | 3 0 5 | 6 0 0 | 0 0 0 |
  |-----------------------|
D | 5 0 0 | 0 4 6 | 0 7 0 |
E | 2 6 0 | 0 0 8 | 5 0 3 |
F | 1 8 7 | 0 0 0 | 0 0 0 |
  |-----------------------|
G | 0 2 6 | 0 0 0 | 0 0 5 |
H | 7 1 8 | 9 0 0 | 0 0 2 |
I | 0 5 0 | 0 6 2 | 7 0 0 |
  +-----------------------+

Edit which cell? (0 = space)
LETTER=ROW -:- NUMBER=COLUMN
 => ENTER 0 TO EXIT
ROW: <enter letter>
COLUMN: <enter number>
New Number: <enter number>
```
