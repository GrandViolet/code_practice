"""
Play the game of Minesweeper

V Buckley
05.20.2024
"""



import random

remainingMines = -1
settings = {
    "Mercy": True,
    "Easy fill": True,
    "Assisted start": False,
    "Mine move random": False,
}



def main():
    menuPrompt = "MINESWEEPER"
    menuOptions = ["Play", "Settings", "Quit"]
    menuOptionChoices = ["play", "settings", "quit"]
    
    loop = True

    while (loop):
        menuOption = get_string_selection(menuPrompt, menuOptions, 
            menuOptionChoices)

        if (menuOption == "play"):
            play_option()
        
        elif (menuOption == "settings"):
            settings_option()
        
        else:
            loop = False

    print()



def play_minesweeper(board, currentBoard, mines):
    """
    Allow the user to play minesweeper with the generated board
    """

    global remainingMines
    mode = "Reveal"
    firstClick = True

    remainingMines = mines

    won = False
    deathCoords = [-1, -1]

    while ((not won) and (deathCoords == [-1, -1])):
        print("\nMines Remaining: %d" % (remainingMines))
        print_board(currentBoard)
        
        print("\nCurrent mode: %s (ENTER to switch)" % (mode))

        xSelection = get_int_quit("X", 1, len(board))

        if (xSelection == -1):
            mode = switch_mode(mode)

        else:
            ySelection = get_int_quit("Y", 1, len(board[0]))

            if (ySelection == -1):
                mode = switch_mode(mode)
                
            else:
                realX = xSelection - 1
                realY = len(board[0]) - ySelection

                if (mode == "Flag"):
                    flag_mode(currentBoard, realX, realY)
                    
                else:
                    deathCoords = reveal_mode(board, currentBoard, realX, 
                        realY, firstClick)
                    firstClick = False
                    
                won = check_victory(board, currentBoard)
    
    return deathCoords


def play_option():
    """
    Menu option to play Minesweeper
    """
    
    difficultyPrompt = "Please select a difficulty"
    difficulties = ["Beginner", "Intermediate", "Expert", "Custom"]
    difficultyChoices = ["beginner", "intermediate", "expert", "custom"]

    difficulty = get_string_selection(difficultyPrompt, difficulties, 
        difficultyChoices)

    if (difficulty == "beginner"):
        width = 8
        height = 8
        mines = 10

    elif (difficulty == "intermediate"):
        width = 16
        height = 16
        mines = 40

    elif (difficulty == "expert"):
        width = 30
        height = 16
        mines = 99

    else:
        print()

        width = get_int("Width of the game board", 1, 99)
        height = get_int("Height of the game board", 1, 99)
        mines = get_int("Number of mines", 0, width * height)

    board = generate_game(width, height, mines)

    currentBoard = generate_blank_board(board)

    deathCoords = play_minesweeper(board, currentBoard, mines)
    
    finalBoard = final_board(board, currentBoard, deathCoords)

    if (deathCoords == [-1, -1]):
        print_board(currentBoard)
        print("\nCongratulations! You win!")
    
    else:
        print("\nSorry! You lose!")
    
    print_board(finalBoard)


def settings_option():
    """
    Allow the user to change the game settings
    """

    global settings

    loop = True

    while (loop):
        print("\nSettings")

        print("  -(1) Mercy: %s" % (settings["Mercy"]))
        print("  -(2) Easy fill: %s" % (settings["Easy fill"]))
        print("  -(3) Assisted start: %s" % (settings["Assisted start"]))
        print("  -(4) Mine move random: %s" % (settings["Mine move random"]))
        
        print("\n  -(5) Reset to defaults")
        print("  -(6) Back")

        print()
        setting = get_int("Choice", 1, 6)

        if (setting == 1):
            settings["Mercy"] = not settings["Mercy"]

        elif (setting == 2):
            settings["Easy fill"] = not settings["Easy fill"]

        elif (setting == 3):
            settings["Assisted start"] = not settings["Assisted start"]

        elif (setting == 4):
            settings["Mine move random"] = not settings["Mine move random"]
        
        elif (setting == 5):
            settings["Mercy"] = True
            settings["Easy fill"] = True
            settings["Assisted start"] = False
        
        else:
            loop = False


def get_string_selection(prompt, strings, stringChoices):
    """
    Get input from the user to select a string from a list
    """

    print("\n%s" % (prompt))

    validInput = False

    while (not validInput):
        for i in range(len(strings)):
            print("  -%s" % (strings[i]))

        userInput = input("\n").lower()

        if (userInput in stringChoices):
            validInput = True

        if (not validInput):
            print("\nPlease select a valid option")
    
    return userInput


def get_int(prompt, low, high):
    """
    Get user input of an integer between lowest and highest, inclusive
    """

    validInput = False

    while (not validInput):
        userInput = input("%s: " % (prompt))

        if (userInput.isdigit()):
            userInputInt = int(userInput)

            if (userInputInt >= low):
                if (userInputInt <= high):
                    validInput = True

        if (not validInput):
            print("Please enter an int between %d and %d" % (low, high))
    
    return userInputInt


def generate_game(width, height, mines):
    """
    Generate the Minesweeper game board
    """

    board = []

    for i in range(width):
        board.append([])

        for j in range(height):
            board[i].append(0)
    
    mineCounter = 0

    while (mineCounter < mines):
        mineX = random.randint(0, width - 1)
        mineY = random.randint(0, height - 1)

        if (board[mineX][mineY] != -1):
            board[mineX][mineY] = -1
            mineCounter += 1
    
    update_neighbor_counts(board)

    return board


def print_board(board):
    """
    Print the game board
    """

    widthNums = "      "
    for i in range(len(board)):
        widthNums += " %2d" % (i + 1)

    print(widthNums)

    horizontalBorder = "     +-"
    horizontalBorder += "---" * len(board)
    horizontalBorder += "-+"

    print(horizontalBorder)

    for i in range(len(board[0])):
        boardLine = " %2d  | " % (len(board[0]) - i)

        for j in range(len(board)):
            if (board[j][i] == -4):
                boardLine += "💥 "

            elif (board[j][i] == -3):
                boardLine += " - "
            
            elif (board[j][i] == -2):
                boardLine += " 🚩"
            
            elif (board[j][i] == -1):
                boardLine += "💣 "
            
            elif (board[j][i] == 0):
                boardLine += "   "

            else:
                boardLine += " " + str(board[j][i]) + " "

        boardLine += " |  %-2d" % (len(board[0]) - i)
        
        print(boardLine)
    
    print(horizontalBorder)
    print(widthNums)


def count_neighbors(board, x, y, cellType):
    """
    Count the number of neighboring cells of a given type to a given cell
    """
    
    counter = 0

    for i in range(-1, 2):
        if (((x + i) >= 0) and ((x + i) < len(board))):
            for j in range(-1, 2):
                if (((y + j) >= 0) and ((y + j) < len(board[0]))):
                    if board[x + i][y + j] == cellType:
                        counter += 1
    
    return counter


def generate_blank_board(board):
    """
    Generate the blank board to correspond to what the player has learned so 
        far
    """
    
    blankBoard = []

    for i in range(len(board)):
        blankBoard.append([])

        for j in range(len(board[0])):
            blankBoard[i].append(-3)
    
    return blankBoard
    

def get_int_quit(prompt, low, high):
    """
    Get user input of an integer between lowest and highest, inclusive
    Return -1 if nothing is entered to trigger a mode switch
    """
    
    validInput = False

    while (not validInput):
        userInput = input("%s: " % (prompt))

        if (userInput == ""):
            userInputInt = -1
            validInput = True
        
        else:
            if (userInput.isdigit()):
                userInputInt = int(userInput)

                if (userInputInt >= low):
                    if (userInputInt <= high):
                        validInput = True

        if (not validInput):
            print("Please enter an int between %d and %d" % (low, high))
    
    return userInputInt


def check_victory(board, currentBoard):
    """
    Check to see if the user has won
    """

    won = True

    for i in range(len(board)):
        for j in range(len(board[0])):
            if (board[i][j] != -1):
                if (board[i][j] != currentBoard[i][j]):
                    won = False

    return won


def flood_fill(board, currentBoard, x, y):
    """
    Reveal all of the cells that are 0 and their neighbors around the selected 
        cell
    """
    
    if ((x >= 0) and (x < len(board))):
        if ((y >= 0) and (y < len(board[0]))):
            if (currentBoard[x][y] == -3):
                currentBoard[x][y] = board[x][y]

                if (board[x][y] == 0):
                    flood_fill(board, currentBoard, x - 1, y - 1)
                    flood_fill(board, currentBoard, x - 1, y + 0)
                    flood_fill(board, currentBoard, x - 1, y + 1)
                    flood_fill(board, currentBoard, x + 0, y - 1)
                    flood_fill(board, currentBoard, x + 0, y + 1)
                    flood_fill(board, currentBoard, x + 1, y - 1)
                    flood_fill(board, currentBoard, x + 1, y + 0)
                    flood_fill(board, currentBoard, x + 1, y + 1)
    

def reveal(board, currentBoard, x, y, deathCoords, firstClick):
    """
    Reveal a cell
    """

    if (firstClick):
        if ((settings["Assisted start"]) and ((board[x][y]) != 0)):
            assisted_start(board, x, y)

        elif ((settings["Mercy"]) and ((board[x][y]) == -1)):
            mercy(board, x, y)
            

    if (board[x][y]) == -1:
        deathCoords = [x, y]
    
    else:
        flood_fill(board, currentBoard, x, y)
    
    return deathCoords


def reveal_around(board, currentBoard, x, y, deathCoords, firstClick):
    """
    Reveal all of the surrounding cells to a selected cell
    """
    
    for i in [-1, 0, 1]:
        if (((x + i) >= 0) and ((x + i) < len(board))):
            for j in [-1, 0, 1]:
                if (((y + j) >= 0) and ((y + j) < len(board[0]))):
                    if (currentBoard[x + i][y + j] == -3):
                        flags = count_neighbors(currentBoard, x, y, -2)

                        if (flags >= board[x][y]):
                            deathCoords = reveal(board, currentBoard, x + i,
                                y + j, deathCoords, firstClick)
    
    return deathCoords


def switch_mode(mode):
    """
    Switch gamemodes
    """
    
    if (mode == "Flag"):
        mode = "Reveal"

    else:
        mode = "Flag"

    return mode


def flag_mode(currentBoard, x, y):
    """
    Control what happens when a cell is selected while in flag mode
    """

    global remainingMines
    
    if (currentBoard[x][y] == -3):
        currentBoard[x][y] = -2
        remainingMines -= 1
    
    elif (currentBoard[x][y] == -2):
        currentBoard[x][y] = -3
        remainingMines += 1


def reveal_mode(board, currentBoard, x, y, firstClick):
    """
    Control what happens when a cell is selected while in reveal mode
    """

    global remainingMines

    deathCoords = [-1, -1]

    if (currentBoard[x][y] == -3):
        deathCoords = reveal(board, currentBoard, x, y, deathCoords, 
            firstClick)
    
    elif ((currentBoard[x][y] > 0) and (settings["Easy fill"])):
        deathCoords = reveal_around(board, currentBoard, x, y, deathCoords, 
            firstClick)   
    
    return deathCoords


def final_board(board, currentBoard, deathCoords):
    """
    Generate the final, ending board to be displayed if the user won or lost
    """

    finalBoard = generate_blank_board(board)

    if (deathCoords == [-1, -1]):
        for i in range(len(finalBoard)):
            for j in range(len(finalBoard[0])):
                if (currentBoard[i][j] == -3):
                    finalBoard[i][j] = board[i][j]

                elif (currentBoard[i][j] == -2):
                    finalBoard[i][j] = -2

                else:
                    finalBoard[i][j] = board[i][j]
            
    else:
        for i in range(len(finalBoard)):
            for j in range(len(finalBoard[0])):
                if (currentBoard[i][j] == -3):
                    finalBoard[i][j] = board[i][j]

                elif (currentBoard[i][j] == -2):
                    if (board[i][j] == -1):
                        finalBoard[i][j] = -2

                    else:
                        finalBoard[i][j] = board[i][j]

                else:
                    finalBoard[i][j] = board[i][j]

        finalBoard[deathCoords[0]][deathCoords[1]] = -4

    return finalBoard


def mercy(board, x, y):
    """
    Remove the bomb from the clicked location if it is the first click, if 
        possible
    """

    board[x][y] = 0

    if (settings["Mine move random"]):
        loop = True

        while (loop):
            mineX = random.randint(0, len(board) - 1)
            mineY = random.randint(0, len(board[0]) - 1)

            if ((mineX != x) or (mineY != y)):
                if (board[mineX][mineY] != -1):
                    board[mineX][mineY] = -1
                    loop = False
    
    else:
        loop = True
        i = 0
        j = 0

        while (loop):
            if (i != x) or (j != y):
                if (board[i][j] != -1):
                    loop = False

            if (loop == True):
                i += 1

                if (i >= (len(board))):
                    i = 0
                    j += 1

                    if (j >= (len(board[0]))):
                        i = x
                        j = y
                        loop = False

        board[i][j] = -1

    update_neighbor_counts(board)


def update_neighbor_counts(board):
    for l in range(len(board)):
        for m in range(len(board[0])):
            if (board[l][m] >= 0):
                neighbors = count_neighbors(board, l, m, -1)
                board[l][m] = neighbors


def assisted_start(board, x, y):
    """
    Assist the user so that their first click is always a zero (or best case 
        scenario if not possible)
    """

    k = 0
    l = 0
    
    for i in [-1, 0, 1]:
        if (((x + i) >= 0) and ((x + i) < len(board))):
            for j in [-1, 0, 1]:
                if (((y + j) >= 0) and ((y + j) < len(board[0]))):
                    if board[x + i][y + j] == -1:
                        board[x + i][y + j] = 0

                        if (settings["Mine move random"]):
                            loop = True

                            while (loop):
                                mineX = random.randint(0, len(board) - 1)
                                mineY = random.randint(0, len(board[0]) - 1)

                                if ((mineX < x - 1) or (mineX > x + 1)):
                                    if ((mineY < y - 1) or (mineY > y + 1)):
                                        if (board[mineX][mineY] != -1):
                                            board[mineX][mineY] = -1
                                            loop = False
                        
                        else:
                            loop = True

                            while (loop):
                                if (k not in [x - 1, x, x + 1]) or \
                                    (l not in [y - 1, y, y + 1]):
                                    if (board[k][l] != -1):
                                        loop = False
                                
                                if (loop == True):
                                    k += 1

                                    if (k >= (len(board))):
                                        k = 0
                                        l += 1

                                        if (l >= (len(board[0]))):
                                            k = x + i
                                            l = y + j
                                            loop = False

                            board[k][l] = -1

    if (board[x][y] == -1):
        mercy(board, x, y)

    update_neighbor_counts(board)



main()