/*
 *  Testing out ncurses
 *  Following along with the "ncurses tutorials" series by Casual Coder
 *  https://www.youtube.com/playlist?list=PL2U2TQ__OrQ8jTf0_noNKtHMuYlyxQl4v
 *  
 *  V. Buckley
 *  Started: 07.02.2024
 * 
 *  v0.600
 */

#include <ncurses.h>

int main() {
    int xMax, yMax;
    char *menuOptions[3] = {"Option 1", "Option 2", "Option 3"};
    int userInput;
    int highlight = 0;
    int i;
    int menuLoop = 1;

    initscr();
    noecho();
    cbreak();

    getmaxyx(stdscr, yMax, xMax);

    WINDOW *window = newwin(6, xMax - 12, yMax - 8, 5);
    box(window, 0, 0);
    refresh();
    wrefresh(window);

    keypad(window, 1);

    while (menuLoop) {
        for (i = 0; i < 3; i++) {
            if (i == highlight) {
                wattron(window, A_REVERSE);
            }

            mvwprintw(window, i + 1, 2, "%s", menuOptions[i]);
            wattroff(window, A_REVERSE);
        }

        userInput = wgetch(window);

        if (userInput == KEY_UP) {
            if (highlight > 0) {
                highlight--;
            }
        } else if (userInput == KEY_DOWN) {
            if (highlight < 2) {
                highlight++;
            }
        } else if (userInput == 10) {
            menuLoop = 0;
        }
    }

    printw("Selected: %s", menuOptions[highlight]);

    getch();
    endwin();
    return 0;
}

/*
    NCURSES FUNCTIONS

        initscr();                                                                                                      // initialize ncurses
        move(yPos, xPos);                                                                                               // move the cursor
        printw("Hello world");                                                                                          // print to the screen
        refresh();                                                                                                      // refresh the screen
        getch();                                                                                                        // wait for user input; return pressed key
        clear();                                                                                                        // clear the screen
        mvprintw(0, 0, "%d", key);                                                                                      // move and printw
        endwin();                                                                                                       // end ncurses

        newwin(height, width, startY, startX);                                                                          // create a new window; return window pointer
        box(window, 0, 0);                                                                                              // print a box within a window
        wprintw(window, "wow, cool box");                                                                               // print within a specified window
        mvwprintw(window, 1, 1, "wow, cool box");                                                                       // move and wprintw
        wrefresh(window);                                                                                               // refresh a specified window

        cbreak();                                                                                                       // allow ctrl+c to close the window (default)
        raw();                                                                                                          // do not allowed ctrl+c to close the window
        noecho();                                                                                                       // do not print ant inputted characters to the screen
        wborder(window, left, right, top, bottom, topLeftCorner, topRightCorner, bottomLeftCorner, bottomRightCorner);  // print a box with specified characters for each of the segments

        has_colors();                                                                                                   // return true if the terminal in use supports colored text
        start_color();                                                                                                  // initalize default colors
        init_pair(1, COLOR_MAGENTA, COLOR_WHITE);                                                                       // initalize a color pair to load when needed
        can_change_color();                                                                                             // return true if the terminal in use supports any color of text
        init_color(COLOR_MAGENTA, 599, 0, 599);                                                                         // initializes a new text color
        attron(A_REVERSE);                                                                                              // turn on a specified attribute
        attroff(A_REVERSE);                                                                                             // turn off a specified attribute
 
        getyx(window, y, x);                                                                                            // set x and y to the current cursor position
        getbegyx(window, yBeg, xBeg);                                                                                   // set xBeg and yBeg to the beginning coordinates of the window
        getmaxyx(window, yMax, xMax);                                                                                   // set xMax and yMax to the maximum coorinates of the window

        keypad(window, 1);                                                                                              // initalize shorthand for non-character button presses
        wgetch(window);                                                                                                 // wait for user input from a specified window; return pressed key

        wattron(window, A_REVERSE);                                                                                     // apply the specified attribute in a specified window
        wattroff(window, A_REVERSE);                                                                                    // remove a specified attribute from a speicied window
 */