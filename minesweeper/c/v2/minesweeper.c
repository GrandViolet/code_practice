/*
 * Play the game of Minesweeper
 * Visualizations done using ncurses
 * 
 * V. Buckley
 * Started: 07.03.2024
 * 
 * v2.001
 */



/******************************* Header Files *******************************/

#include <ncurses.h>

/*************************** Function Prototypes ***************************/

void menu(WINDOW *window);


/******************************** Functions ********************************/

int main() {
    initscr();
    noecho();
    cbreak();
    start_color();
    curs_set(0);

    int yMax, xMax;

    getmaxyx(stdscr, yMax, xMax);

    WINDOW *window = newwin(yMax - 2, xMax - 2, 1, 1);
    refresh();
    keypad(window, 1);

    menu(window);

    endwin();
    return 0;
}

/* Contol the main menu */
void menu(WINDOW *window) {
    int menuLoop = 1, selected = 0, options = 3;
    int i, key;
    char *menuOptions[] = {"Play", "Settings", "Quit"};

    box(window, 0, 0);

    while (menuLoop) {
        for (i = 0; i < options; i++) {
            if (i == selected) {
                mvwprintw(window, 1 + i, 2, "> %s", menuOptions[i]);
            } else {
                mvwprintw(window, 1 + i, 2, "  %s", menuOptions[i]);
            }
        }

        wrefresh(window);

        key = wgetch(window);

        if (key == 10) {
            menuLoop = 0;
        } else if (key == KEY_UP) {
            if (selected > 0) {
                selected--;
            }
        } else if (key == KEY_DOWN) {
            if (selected < options - 1) {
                selected++;
            }
        }
    }

}