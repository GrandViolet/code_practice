/*
 * Play the game of Minesweeper
 * 
 * V Buckley
 * Started: 05.29.2024
 * 
 * v1.110
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


/*
 * All of the editable settings options
 */
struct settingsData {

    int setSeed;

    int mercy;
    int easyFill;
    int assistedStart;
    int mineMoveRandom;
};




/*************************** Function Prototypes ***************************/

void generate_game(struct minesweeperData *data, struct settingsData *settings);
void play_minesweeper(struct minesweeperData *data);
void print_board(struct minesweeperData *data, int *board);
void generate_blank_board(struct minesweeperData *data);
void update_neighbor_counts(struct minesweeperData *data);
int count_neighbors(struct minesweeperData *data, int i, int j, int type);
int get_int_input(unsigned int low, unsigned int high);
int difficultyManager(struct minesweeperData *data);
int main_menu(struct minesweeperData *data, struct settingsData *settings);
void print_title();
int menu_selector();




/******************************** Functions ********************************/

int main() {

    int loop = 1, ret;
    struct minesweeperData data;
    struct settingsData settings;

    while (loop) {
        ret = main_menu(&data, &settings);
            
        play_minesweeper(&data);

        free(data.board);
        free(data.currentBoard);

        loop = 0;
    }

    return 0;
}



/*
 * Generate the Minesweeper game board
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 *      settings (settingsData *) - the editable settings that the user can control
 * Ret:
 *      None
 */
void generate_game(struct minesweeperData *data, struct settingsData *settings) {
    
    int i = 0, seed, mineCounter = 0, cellIdx;

    (data->board) = malloc(sizeof(int) * ((data->width) * (data->height)));

    if (!(data->board)) {
        perror("\nERROR: malloc failed");
        exit(1);
    }

    for (i; i < ((data->width) * (data->height)); i++) {
        (data->board)[i] = 0;
    }

    if ((settings->setSeed) == 1) {
        srand(time(NULL));

    } else {
        seed = get_int_input(0, 4294967295);
        srand(seed);
    }

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

    int loop = 1, x, y;

    print_board(data, (data->board));

    while (loop) {
        print_board(data, (data->currentBoard));

        printf("\nReveal mode (enter 0 to switch modes)\n");

        printf("\nPlease select a column (x):\n");
        x = get_int_input(0, (data->width));

        if (!x) {
            printf("DEBUG: mode swap\n");

        } else {
            printf("\nPlease select a row (y):\n");
            y = get_int_input(0, (data->height));

            if (!y) {
                printf("DEBUG: mode swap\n");
            
            } else {
                printf("DEBUG: reveal\n");

                loop = 0;
            }
        }
    }

}


/*
 * Print the game board
 * Args:
 *      data (minesweeperData *) - the struct containing all of the Minesweeper board data
 * Ret:
 *      None
 */
void print_board(struct minesweeperData *data, int *board) {

    int i = 0, j, cellNum;

    printf("     ");
    for (i; i < (data->width); i++) {
        printf(" %-2d", i + 1);
    }
    printf("\n");

    printf("   +-");
    for (i = 0; i < (data->width); i++) {
        printf("---");
    }
    printf("-+\n");
    
    for (i = 0; i < (data->height); i++) {
        printf("%2d | ", ((data->height) - i));

        for (j = 0; j < (data->width); j++) {
            cellNum = board[j + (i * (data->width))];
            
            if ((cellNum >= 0) && (cellNum <= 8)) {     // Number (0-8)
                if (cellNum == 0) {         // Blank (8)
                    printf("\033[8m");
                
                } else if (cellNum == 1) {  // Blue (34)
                    printf("\033[34m");
                
                } else if (cellNum == 2) {  // Green (32)
                    printf("\033[32m");
                
                } else if (cellNum == 3) {  // Red (31)
                    printf("\033[31m");
                
                } else if (cellNum == 4) {  // Darkened Blue (2;34)
                    printf("\033[2;34m");
                
                } else if (cellNum == 5) {  // Darkened Red (2;31)
                    printf("\033[2;31m");
                
                } else if (cellNum == 6) {  // Cyan (36)
                    printf("\033[36m");
                
                } else if (cellNum == 7) {  // Darkened White (2)
                    printf("\033[2;90m");
                
                } else {                    // White (37)
                    printf("\033[2;37m");
                }

                printf("\033[1m %d \033[m", cellNum);
            
            } else if (cellNum == 9) {                  // Mine (9)
                printf("💣 ");

            } else if (cellNum == 10) {                 // Flag (10)
                printf(" 🚩");

            } else if (cellNum == 11) {                 // Hidden (11)
                printf("\033[2;90m - \033[m");

            } else if (cellNum == 12) {                 // Explosion (12)
                printf("💥 ");

            } else {
                fprintf(stderr, "\nERROR: Unexpected value in found in game board");
                exit(1);
            }
        }

        printf(" | %d\n", ((data->height) - i));
    }

    printf("   +-");
    for (i = 0; i < (data->width); i++) {
        printf("---");
    }
    printf("-+\n");

    printf("     ");
    for (i = 0; i < (data->width); i++) {
        printf(" %-2d", i + 1);
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

    int i = 0;

    (data->currentBoard) = malloc(sizeof(int) * ((data->width) * (data->height)));

    if (!(data->currentBoard)) {
        perror("\nERROR: malloc failed");
        exit(1);
    }

    for (i; i < ((data->width) * (data->height)); i++) {
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

    int i = 0, j, cellNum, neighbors;
    
    for (i; i < (data->height); i++) {
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

    int counter = 0, colOffset = -1, rowOffset;
    
    for (colOffset; colOffset <= 1; colOffset++) {
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
int get_int_input(unsigned int low, unsigned int high) {

    int validInput = 0;
    unsigned int num;
    char *ret;
    char userInput[MAXLENGTH];

    while(!validInput) {
        printf("Enter an int between %d and %u: ", low, high);
        fflush(stdout);

        ret = fgets(userInput, MAXLENGTH, stdin);
        if ((ferror(stdin)) || (!ret)) {
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
int difficultyManager(struct minesweeperData *data) {
    
    int difficulty, ret = 0;

    printf("\nPlease select a difficulty:\n");
    printf("  0) Back\n");
    printf("  1) Beginner\n");
    printf("  2) Intermediate\n");
    printf("  3) Expert\n");
    printf("  4) Custom\n\n");

    difficulty = get_int_input(0, 4);

    if (difficulty == 0) {
        ret = 1;

    } else if (difficulty == 1) {
        (data->width) = 8;
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

    return ret;
}


/*
 * Control the main menu of the game, allowing the user to change settings and begin playing
 * Args:
 *      data (minesweeperData *) - the current game data struct
 *      settings (settingsData *) - the editable settings that the user can control
 * Ret:
 *      ret (int) - TODO
 */
int main_menu(struct minesweeperData *data, struct settingsData *settings) {

    int selection, ret;

    print_title();

    selection = menu_selector();

    if (selection == 1) {
        ret = difficultyManager(data);

            if(ret == 0) {
                generate_game(data, settings);
                generate_blank_board(data);
            }
    }

    return ret;
}


/*
 * Print the title art and creator
 * Args:
 *      None
 * Ret:
 *      None
 */
void print_title() {
    
    printf("\n");
    printf(" ___________ _______ _______ _______ _______ ___   _   _ _______ _______ _______ _______ _______\n");
    printf("|    _   _  |_     _|    _  |    ___|    ___|   | | | | |    ___|    ___|    _  |    ___|    _  |\n");
    printf("|   | | | | | |   | |   | | |   |___|   |___|   | | | | |   |___|   |___|   |_| |   |___|   |_| |_\n");
    printf("|   | | | | | |   | |   | | |    ___|_____  |   | | | | |    ___|    ___|    ___|    ___|    ___  |\n");
    printf("|   | | | | |_|   |_|   | | |   |___ _____| |   |_| |_| |   |___|   |___|   |   |   |___|   |   | |\n");
    printf("|___| |_| |_|_______|___| |_|_______|_______|___________|_______|_______|___|   |_______|___|   |_|\n");
    printf("                                   Created by Grand Violet, 2024\n");

}


/*
 * Allow the user to select a menu option
 * Args:
 *      None
 * Ret:
 *      selection (int) - the chosen selections
 */
int menu_selector() {
    
    int selection;

    printf("  1) Play\n");
    printf("  2) Settings\n");
    printf("  0) Quit\n");

    selection = get_int_input(0, 2);

    return selection;
}
