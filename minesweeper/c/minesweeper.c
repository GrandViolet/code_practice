/*
 * Play the game of Minesweeper
 * 
 * V Buckley
 * Started: 05.29.2024
 * 
 * v1.105
 */



/******************************* Header Files *******************************/

#include <stdio.h>
#include <stdlib.h>
#include <time.h>




/******************************* Definitions *******************************/

#define MAXLENGTH 1024




/***************************** Global Variables *****************************/

/*
 * All of the data needed to keep track of globally to run each game of Minesweeper
 */
struct minesweeperData {

    int width;
    int height;
    int mines;

    int *board;
    int *currentBoard;
};




/*************************** Function Prototypes ***************************/

void generate_game(struct minesweeperData *data);
void play_minesweeper(struct minesweeperData *data);
void print_board(struct minesweeperData *data, int *board);
void generate_blank_board(struct minesweeperData *data);
void update_neighbor_counts(struct minesweeperData *data);
int count_neighbors(struct minesweeperData *data, int i, int j, int type);
int get_int_input(int low, int high);
void difficultyManager(struct minesweeperData *data);




/******************************** Functions ********************************/

int main() {

    struct minesweeperData data;
    int loop;

    srand(time(NULL));
    
    loop = 1;
    while (loop) {
        difficultyManager(&data);
        generate_game(&data);
        generate_blank_board(&data);

        play_minesweeper(&data);
        
        loop = 0;
    }

    free(data.board);
    free(data.currentBoard);

    return 0;
}



/*
 * Generate the Minesweeper game board
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 * Ret:
 *      None
 */
void generate_game(struct minesweeperData *data) {
    
    int i;
    int mineCounter;
    int cellIdx;

    (data->board) = malloc(sizeof(int) * ((data->width) * (data->height)));

    if (!(data->board)) {
        perror("\nERROR: malloc failed");
        exit(1);
    }

    for (i = 0; i < ((data->width) * (data->height)); i++) {
        (data->board)[i] = 0;
    }

    mineCounter = 0;
    while (mineCounter < (data->mines)) {
        cellIdx = rand() % ((data->width) * (data->height));

        if ((data->board)[cellIdx] != 9) {
            (data->board)[cellIdx] = 9;

            mineCounter++;
        }
    }

    update_neighbor_counts(data);

}


/*
 * Allow the user to play minesweeper with the generated board
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 * Ret:
 *      None
 */
void play_minesweeper(struct minesweeperData *data) {

    print_board(data, (data->board));
    print_board(data, (data->currentBoard));

}


/*
 * Print the game board
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 * Ret:
 *      None
 */
void print_board(struct minesweeperData *data, int *board) {

    int i, j, k;
    int cellNum;
    char cell;

    printf("     ");
    for (k = 0; k < (data->width); k++) {
        printf(" %-2d", k + 1);
    }
    printf("\n");

    printf("   +-");
    for (k = 0; k < (data->width); k++) {
        printf("---");
    }
    printf("-+\n");
    
    for (i = 0; i < (data->height); i++) {
        printf("%2d | ", ((data->height) - i));
        for (j = 0; j < (data->width); j++) {
            cellNum = board[j + (i * (data->width))];
            
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

        printf(" | %d\n", ((data->height) - i));
    }

    printf("   +-");
    for (k = 0; k < (data->width); k++) {
        printf("---");
    }
    printf("-+\n");

    printf("     ");
    for (k = 0; k < (data->width); k++) {
        printf(" %-2d", k + 1);
    }
    printf("\n");

}


/*
 * Generate the blank board to correspond to what the player has learned so far
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 * Ret:
 *      None
 */
void generate_blank_board(struct minesweeperData *data) {

    int i;

    (data->currentBoard) = malloc(sizeof(int) * ((data->width) * (data->height)));

    if (!(data->currentBoard)) {
        perror("\nERROR: malloc failed");
        exit(1);
    }

    for (i = 0; i < ((data->width) * (data->height)); i++) {
        (data->currentBoard)[i] = 11;
    }

}


/*
 * Count the number of mines neighboring each cell and update their values accordingly
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 * Ret:
 *      None
 */
void update_neighbor_counts(struct minesweeperData *data) {

    int i, j;
    int cellNum;
    int neighbors;
    
    for (i = 0; i < (data->height); i++) {
        for (j = 0; j < (data->width); j++) {
            cellNum = (data->board)[j + (i * (data->width))];

            if (cellNum <= 8) {
                neighbors = count_neighbors(data, i, j, 9);
                (data->board)[j + (i * (data->width))] = neighbors;
            }
        }
    }

}


/*
 * Count the number of neighboring cells of a given type to a given cell
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 *      i (int) - the row of the cell that is being checked
 *      j (int) - the column of the cell that is being checked
 *      type (int) - the type of cell we are searching for in the neighbors
 * Ret:
 *      counter (int) - the number of neighboring cells of the given type
 */
int count_neighbors(struct minesweeperData *data, int i, int j, int type) {

    int colOffset, rowOffset;
    int counter = 0;
    
    for (colOffset = -1; colOffset <= 1; colOffset++) {
        if ((j + colOffset >= 0) && (j + colOffset < (data->width))) {
            for (rowOffset = -1; rowOffset <= 1; rowOffset++) {
                if ((i + rowOffset >= 0) && (i + rowOffset < (data->height))) {
                    if ((data->board)[(colOffset + j) + ((rowOffset + i) * (data->width))] == type) {
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
    int validInput;

    validInput = 0;
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


/*
 * Set all relevant data depending on the user selected difficulty 
 * Args:
 *      data (minesweeperData *) - the current game data struct
 * Ret:
 *      None
 */
void difficultyManager(struct minesweeperData *data) {
    
    int difficulty = get_int_input(1, 4);

    printf("HERE 1\n");

    if (difficulty == 1) {
        printf("HERE 2\n");
        (data->width) = 8;
        printf("HERE 3\n");
        (data->height) = 8;
        (data->mines) = 10;
    } else if (difficulty == 2) {
        (data->width) = 16;
        (data->height) = 16;
        (data->mines) = 40;
    } else if (difficulty == 3) {
        (data->width) = 30;
        (data->height) = 16;
        (data->mines) = 99;
    } else if (difficulty == 4) {
        (data->width) = get_int_input(1, 99);
        (data->height) = get_int_input(1, 99);
        (data->mines) = get_int_input(0, ((data->width) * (data->height)));
    } else {
        fprintf(stderr, "\nERROR: invalid difficulty setting");
        exit(1);
    }

}
