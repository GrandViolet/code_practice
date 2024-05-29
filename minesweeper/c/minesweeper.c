/*
 * Play the game of Minesweeper
 * 
 * V Buckley
 * 05.29.2024
 * 
 * v1.1
 */



/******************************* Header Files *******************************/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>



/*************************** Function Prototypes ***************************/
int *generate_game(int width, int height, int mines);
void play_minesweeper(int *board);
void print_board(int width, int height, int *board);
int *generate_blank_board(int width, int height);



/******************************** Functions ********************************/
int main() {
    printf("DEBUG: in main\n");

    int loop = 1;
    time_t t;
    int *board;
    int *currentBoard;

    srand((unsigned) time(&t));

    while(loop) {
        int width = 8;
        int height = 8;
        int mines = 10;

        board = generate_game(width, height, mines);

        play_minesweeper(board);
        currentBoard = generate_blank_board(width, height);

        print_board(width, height, currentBoard);
        
        loop = 0;
    }

    free(board);
    return 0;
}


int *generate_game(int width, int height, int mines) {
    /*
     * Generate the Minesweeper game board
     */
    printf("DEBUG: in generate_game\n");

    int *board = malloc(sizeof(int) * (width * height));

    if (!board) {
        printf("\nERROR: malloc failed!\n\n");
        exit(1);
    }

    int i = 0;
    while (++i <= (width * height)) {
        board[i - 1] = 0;
    }

    int mineCounter = 0;
    while (mineCounter < mines) {
        int r = rand() % ((width * height));

        if (board[r] != 9) {
            board[r] = 9;
            mineCounter++;
        }
    }

    return board;
}


void play_minesweeper(int *board) {
    /*
     * Allow the user to play minesweeper with the generated board
     */
    printf("DEBUG: in play_minesweeper\n");

}


void print_board(int width, int height, int *board) {
    /*
     * Print the game board
     */
    printf("DEBUG: in print_board\n");

    int cellNum;
    char cell;

    int i = 0;
    while (++i <= height) {
        int j = 0;
        while (++j <= width) {
            cellNum = board[(j - 1) + ((i - 1) * width)];
            
            if (cellNum == 0) {                             // Empty
                cell = ' ';
            } else if ((cellNum >= 1) && (cellNum <= 8)) {  // Number
                cell = cellNum + 48;
            } else if (cellNum == 9) {                      // Bomb
                cell = 'B';
            } else if (cellNum == 10) {                     // Flag
                cell = 'F';
            } else if (cellNum == 11) {                     // Hidden
                cell = '-';
            } else if (cellNum == 12) {                     // Explosion
                cell = 'E';
            } else {
                printf("\nERROR: Unexpected value in found in game board\n\n");
                exit(1);
            }

            printf(" %c ", cell);
        }

        printf("\n");
    }
}


int *generate_blank_board(int width, int height) {
    /*
     * Generate the blank board to correspond to what the player has learned so far
     */
    printf("DEBUG: in generate_blank_board\n");

    int *currentBoard = malloc(sizeof(int) * (width * height));

    if (!currentBoard) {
        printf("\nERROR: malloc failed!\n\n");
        exit(1);
    }

    int i = 0;
    while (++i <= (width * height)) {
        currentBoard[i - 1] = 11;
    }

    return currentBoard;

}