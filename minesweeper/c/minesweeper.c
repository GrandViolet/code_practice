/*
 * Play the game of Minesweeper
 * 
 * V Buckley
 * Started: 05.29.2024
 * 
 * v1.104
 */



/******************************* Header Files *******************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>




/******************************* Definitions *******************************/

#define MAXLENGTH 1024




/*************************** Function Prototypes ***************************/

int *generate_game(int width, int height, int mines);
void play_minesweeper(int width, int height, int *board, int* currentBoard);
void print_board(int width, int height, int *board);
int *generate_blank_board(int width, int height);
void update_neighbor_counts(int width, int height, int *board);
int count_neighbors(int width, int height, int *board, int i, int j, int type);
int get_int_input(int low, int high);




/******************************** Functions ********************************/

int main() {

    int loop = 1;
    int difficulty = 1;
    int width, height, mines;

    int *board;
    int *currentBoard;

    srand(time(NULL));

    get_int_input(1, 2);

    while (loop) {
        if (difficulty == 0) {
            width = 8;
            height = 8;
            mines = 10;
        } else if (difficulty == 1) {
            width = 16;
            height = 16;
            mines = 40;
        } else if (difficulty == 2) {
            width = 30;
            height = 16;
            mines = 99;
        } else {
            fprintf(stderr, "\nERROR: invalid difficulty setting");
            exit(1);
            //     print()

            //     width = get_int("Width of the game board", 1, 99)
            //     height = get_int("Height of the game board", 1, 99)
            //     mines = get_int("Number of mines", 0, width * height)
        }

        board = generate_game(width, height, mines);

        currentBoard = generate_blank_board(width, height);

        play_minesweeper(width, height, board, currentBoard);
        
        loop = 0;
    }

    free(board);
    free(currentBoard);

    return 0;
}



/*
 * Generate the Minesweeper game board
 * Args:
 *      width (int) - the width of the Minesweeper board
 *      height (int) - the height of the Minesweeper board
 *      mines (int) - the number of mines to be placed on the board
 * Ret:
 *      board (int *) - the game board, where each cell is either a mine (9) or the number of neighboring mines (1-8)
 */
int *generate_game(int width, int height, int mines) {

    int *board = malloc(sizeof(int) * (width * height));

    if (!board) {
        perror("\nERROR: malloc failed");
        exit(1);
    }

    for (int i = 0; i < (width * height); i++) {
        board[i] = 0;
    }

    int mineCounter = 0;
    while (mineCounter < mines) {
        int r = rand() % ((width * height));

        if (board[r] != 9) {
            board[r] = 9;

            mineCounter++;
        }
    }

    update_neighbor_counts(width, height, board);

    return board;
}


/*
 * Allow the user to play minesweeper with the generated board
 * Args:
 *      width (int) - the width of the Minesweeper board
 *      height (int) - the height of the Minesweeper board
 *      board (int *) - the completed Minesweeper board
 *      currentBoard (int *) - the current state of the Minesweeper board
 * Ret:
 *      None
 */
void play_minesweeper(int width, int height, int *board, int* currentBoard) {

    print_board(width, height, board);
    print_board(width, height, currentBoard);

}


/*
 * Print the game board
 * Args:
 *      width (int) - the width of the Minesweeper board
 *      height (int) - the height of the Minesweeper board
 *      board (int *) - the board to be printed
 * Ret:
 *      None
 */
void print_board(int width, int height, int *board) {

    int cellNum, k;
    char cell;

    printf("     ");
    for (k = 0; k < width; k++) {
        printf(" %-2d", k + 1);
    }
    printf("\n");

    printf("   +-");
    for (k = 0; k < width; k++) {
        printf("---");
    }
    printf("-+\n");
    
    for (int i = 0; i < height; i++) {
        printf("%2d | ", (height - i));
        for (int j = 0; j < width; j++) {
            cellNum = board[j + (i * width)];
            
            if (cellNum == 0) {                             // Empty (0)
                printf(" %c ", ' ');
            } else if ((cellNum >= 1) && (cellNum <= 8)) {  // Number (1-8)
                printf(" %d ", cellNum);
            } else if (cellNum == 9) {                      // Mine (9)
                printf("💣 ");
            } else if (cellNum == 10) {                     // Flag (10)
                printf(" 🚩");
            } else if (cellNum == 11) {                     // Hidden (11)
                printf(" - ");
            } else if (cellNum == 12) {                     // Explosion (12)
                printf("💥 ");
            } else {
                fprintf(stderr, "\nERROR: Unexpected value in found in game board");
                exit(1);
            }
        }

        printf(" | %d\n", (height - i));
    }

    printf("   +-");
    for (k = 0; k < width; k++) {
        printf("---");
    }
    printf("-+\n");

    printf("     ");
    for (k = 0; k < width; k++) {
        printf(" %-2d", k + 1);
    }
    printf("\n");

}


/*
 * Generate the blank board to correspond to what the player has learned so far
 * Args:
 *      width (int) - the width of the Minesweeper board
 *      height (int) - the height of the Minesweeper board
 * Ret:
 *      currentBoard (int *) - the blank board of all unknown cells that the player will begin with
 */
int *generate_blank_board(int width, int height) {

    int *currentBoard = malloc(sizeof(int) * (width * height));

    if (!currentBoard) {
        perror("\nERROR: malloc failed");
        exit(1);
    }

    for (int i = 0; i < (width * height); i++) {
        currentBoard[i] = 11;
    }

    return currentBoard;

}


/*
 * Count the number of mines neighboring each cell and update their values accordingly
 * Args:
 *      width (int) - the width of the Minesweeper board
 *      height (int) - the height of the Minesweeper board
 *      board (int *) - the Minesweeper board with which to update the neighbor countss
 * Ret:
 *      None
 */
void update_neighbor_counts(int width, int height, int *board) {

    int cellNum, neighbors;
    
    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            cellNum = board[j + (i * width)];

            if (cellNum <= 8) {
                neighbors = count_neighbors(width, height, board, i, j, 9);
                board[j + (i * width)] = neighbors;
            }
        }
    }
}


/*
 * Count the number of neighboring cells of a given type to a given cell
 * Args:
 *      width (int) - the width of the Minesweeper board
 *      height (int) - the height of the Minesweeper board
 *      board (int *) - the Minesweeper board to count on
 *      i (int) - the row of the cell that is being checked
 *      j (int) - the column of the cell that is being checked
 *      type (int) - the type of cell we are searching for in the neighbors
 * Ret:
 *      counter (int) - the number of neighboring cells of the given type
 */
int count_neighbors(int width, int height, int *board, int i, int j, int type) {

    int counter = 0;
    
    for (int colOffset = -1; colOffset <= 1; colOffset++) {
        if ((j + colOffset >= 0) && (j + colOffset < width)) {
            for (int rowOffset = -1; rowOffset <= 1; rowOffset++) {
                if ((i + rowOffset >= 0) && (i + rowOffset < height)) {
                    if (board[(colOffset + j) + ((rowOffset + i) * width)] == type) {
                        counter++;
                    }
                }
            }
        }
    }

    return counter;
}


/*
 * Get an integer input from the user between the given low and high values, inclusive
 * Args:
 *      low (int) - the smallest allowed int
 *      high (int) - the largest allowed int
 * Ret:
 *      num (int) - the selected int
 */
int get_int_input(int low, int high) {

    char userInput[MAXLENGTH];
    int num;

    int validInput = 0;
    while(!validInput) {
        printf("Enter an int between %d and %d: ", low, high);
        fflush(stdout);

        fgets(userInput, MAXLENGTH, stdin);

        if (ferror(stdin)) {
            perror("\nERROR: fgets failed");
            exit(1);
        }

        num = atoi(userInput);

        if ((num >= low) && (num <= high)) {
            validInput = 1;
        }
        
    }

    return num;
}
