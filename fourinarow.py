from random import choice

def main():
    height = 6
    width = 7
    winCondition = 4

    print("\nWelcome to Four in a Row!\n")

    statistics = [0, 0, 0]

    while 1 == 1:
        mode = gamemode()
        while mode == -1:
            print_stats(statistics)
            mode = gamemode()
        if mode == 2:
            games = int(input("How many games would you like it to play?\n"))
            gameCount = 0
            while gameCount < games:
                game(mode, height, width, statistics, winCondition)
                gameCount = gameCount + 1
            print_stats(statistics)
        else:
            game(mode, height, width, statistics, winCondition)

def gamemode():
    mode = input("Play | Multiplayer | Auto | Statistics | Quit\n")
    while 1 == 1:
        if mode == "Play" or mode == "play" or mode == "P" or mode == "p":
            return 0
        elif mode == "Multiplayer" or mode == "multiplayer" or mode == "M" or mode == "m":
            return 1
        elif mode == "Auto" or mode == "auto" or mode == "A" or mode == "a":
            return 2
        elif mode == "Statistics" or mode == "statistics" or mode == "S" or mode == "s":
            return -1
        elif mode == "Quit" or mode == "quit" or mode == "Q" or mode == "q":
            print("\nThanks for playing!\n")
            quit()
        else:
            print("Please enter a valid option\n")
            mode = input("Play | Multiplayer | Auto | Statistics | Quit\n")
            
def print_stats(statistics):
    gamesPlayed = statistics[0] + statistics[1] + statistics[2]
    print("\n\nGames Played: %d" % (gamesPlayed))

    print("\nX Wins: %d" % (statistics[0]))
    if gamesPlayed != 0:
        winPercent1 = 100 * statistics[0] / (statistics[0] + statistics[1] + statistics[2])
        print("X Win Percentage: %.2f" % (winPercent1))

    print("\nO Wins: %d" % (statistics[1]))
    if gamesPlayed != 0:
        winPercent2 = 100 * statistics[1] / (statistics[0] + statistics[1] + statistics[2])
        print("O Win Percentage: %.2f" % (winPercent2))

    print("\nTied Games: %d" % (statistics[2]))

    print("\n")

def game(mode, height, width, statistics, winCondition):
    board = []
    for i in range(height * width):
        board.append("-")

    outcome = 0
    while 1 == 1:
        if outcome == 0:
            gamer = "X"
            outcome = player(mode, gamer, height, width, board, winCondition)
        if outcome == 0:
            gamer = "O"
            outcome = player(mode, gamer, height, width, board, winCondition)

        if outcome == 1:
            print()
            print_board(height, width, board)
            print("%s WINS!\n" % gamer)
            if gamer == "X":
                statistics[0] = statistics[0] + 1
            if gamer == "O":
                statistics[1] = statistics[1] + 1
            return
        
        if outcome == 2:
            print()
            print_board(height, width, board)
            print("It's a draw!\n")
            statistics[2] = statistics[2] + 1
            return

def player(mode, gamer, height, width, board, winCondition):
    print("\n%s's turn:" % (gamer))
    print_board(height, width, board)

    if mode == 0 and gamer != "X":
        selection = computer_input(height, width, board)
    elif mode == 2:
        selection = computer_input(height, width, board)
    else:
        selection = player_input(height, width, board)

    for i in range(1, height + 1):
        if board[(selection - 1) + (height - i) * width] == "-":
            board[(selection - 1) + (height - i) * width] = gamer
            break
    if win_condition(board, height, width, winCondition) == True:
        return 1
    elif draw_condition(board) == True:
        return 2
    else:
        return 0

def print_board(height, width, board):
    for i in range(height):
        row = ""
        for j in range(width):
            row = row + str(board[i * width + j]) + " "
        print(row)

def player_input(height, width, board):
    column = 0
    emptySpace = 0
    while (column < 1 or column > width) or emptySpace == 0:
        column = int(input())
        if not(column < 1 or column > width):
            for i in range(height):
                if board[(column - 1) + i * width] == "-":
                    emptySpace = emptySpace + 1
            if emptySpace == 0:
                print("Column is full")
        else:
            print("Please pick a column between 1 and %s" % (width))
    return column       

def computer_input(height, width, board):
    column = 0
    emptySpace = 0
    while (column < 1 or column > width) or emptySpace == 0:
        column = choice(range(width)) + 1
        if not(column < 1 or column > width):
            for i in range(height):
                if board[(column - 1) + i * width] == "-":
                    emptySpace = emptySpace + 1
    return column      

def win_condition(board, height, width, winCondition):
    for columnID in range(0, height * width, width):
        for column in range(0, width - winCondition + 1):
            if board[columnID + column] != "-":
                check = board[columnID + column]
                matchCounter = 0
                for i in range(1, winCondition):
                    if board[columnID + column + i] == check:
                        matchCounter = matchCounter + 1
                    if matchCounter == winCondition - 1:
                        return True
    
    for columnID in range(0, (height - winCondition + 1) * width , width):
        for column in range(0, width):
            if board[columnID + column] != "-":
                check = board[columnID + column]
                matchCounter = 0
                for i in range(width, winCondition * width, width):
                    if board[columnID + column + i] == check:
                        matchCounter = matchCounter + 1
                    if matchCounter == winCondition - 1:
                        return True

    for columnID in range(0, (height - winCondition + 1) * width , width):
        for column in range(0, width - winCondition + 1):
            if board[columnID + column] != "-":
                check = board[columnID + column]
                matchCounter = 0
                for i in range(width + 1, winCondition * width + winCondition, width + 1):
                    if board[columnID + column + i] == check:
                        matchCounter = matchCounter + 1
                    if matchCounter == winCondition - 1:
                        return True
    
    for columnID in range(0, (height - winCondition + 1) * width , width):
        for column in range(winCondition - 1, width):
            if board[columnID + column] != "-":
                check = board[columnID + column]
                matchCounter = 0
                for i in range(width - 1, winCondition * width - winCondition, width - 1):
                    if board[columnID + column + i] == check:
                        matchCounter = matchCounter + 1
                    if matchCounter == winCondition - 1:
                        return True

def draw_condition(board):
    emptySquares = 0
    for square in board:
        if square == "-":
            emptySquares = emptySquares + 1
    if emptySquares == 0:
        return True

main()