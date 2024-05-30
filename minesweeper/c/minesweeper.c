/*
 * Play the game of Minesweeper
 * 
 * V Buckley
 * 05.29.2024
 * 
 * v1.103
 */



/******************************* Header Files *******************************/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>



/*************************** Function Prototypes ***************************/
int *generate_game(int width, int height, int mines);
void play_minesweeper(int width, int height, int *board, int* currentBoard);
void print_board(int width, int height, int *board);
int *generate_blank_board(int width, int height);
void update_neighbor_counts(int width, int height, int *board);
int count_neighbors(int width, int height, int *board, int i, int j, int type);



/******************************** Functions ********************************/
int main() {
    printf("DEBUG: in main\n");

    int loop = 1;
    int difficulty = 1;
    int width, height, mines;

    int *board;
    int *currentBoard;

    srand(time(NULL));

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
            printf("\nERROR: invalid difficulty setting!\n\n");
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



int *generate_game(int width, int height, int mines) {
    /*
     * Generate the Minesweeper game board
     * 
     * Args:
     *      width (int) - the width of the Minesweeper board
     *      height (int) - the height of the Minesweeper board
     *      mines (int) - the number of mines to be placed on the board
     * Ret:
     *      board (int *) - the game board, where each cell is either a mine (9) or the number of neighboring mines (1-8)
     */
    printf("DEBUG: in generate_game\n");

    int *board = malloc(sizeof(int) * (width * height));

    if (!board) {
        printf("\nERROR: malloc failed!\n\n");
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


void play_minesweeper(int width, int height, int *board, int* currentBoard) {
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
    printf("DEBUG: in play_minesweeper\n");

    print_board(width, height, board);
    print_board(width, height, currentBoard);

}


void print_board(int width, int height, int *board) {
    /*
     * Print the game board
     * Args:
     *      width (int) - the width of the Minesweeper board
     *      height (int) - the height of the Minesweeper board
     *      board (int *) - the board to be printed
     * Ret:
     *      None
     */
    printf("DEBUG: in print_board\n");

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
                printf("\nERROR: Unexpected value in found in game board\n\n");
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


int *generate_blank_board(int width, int height) {
    /*
     * Generate the blank board to correspond to what the player has learned so far
     * Args:
     *      width (int) - the width of the Minesweeper board
     *      height (int) - the height of the Minesweeper board
     * Ret:
     *      currentBoard (int *) - the blank board of all unknown cells that the player will begin with
     */
    printf("DEBUG: in generate_blank_board\n");

    int *currentBoard = malloc(sizeof(int) * (width * height));

    if (!currentBoard) {
        printf("\nERROR: malloc failed!\n\n");
        exit(1);
    }

    for (int i = 0; i < (width * height); i++) {
        currentBoard[i] = 11;
    }

    return currentBoard;

}


void update_neighbor_counts(int width, int height, int *board) {
    /*
     * Count the number of mines neighboring each cell and update their values accordingly
     * Args:
     *      width (int) - the width of the Minesweeper board
     *      height (int) - the height of the Minesweeper board
     *      board (int *) - the Minesweeper board with which to update the neighbor countss
     */
    printf("DEBUG: in update_neighbor_counts\n");

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


int count_neighbors(int width, int height, int *board, int i, int j, int type) {
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
    printf("DEBUG: in count_neighbors\n");

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
