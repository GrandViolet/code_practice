from random import choice

def main():
    height = 6
    width = 7
    winCondition = 4

    print("\nWelcome to Four in a Row!\n")

    statistics = [0, 0, 0]

    board = []
    for i in range(height * width):
        board.append("-")

    while 1 == 1:
        mode = gamemode()
        while mode == -1:
            print_stats(statistics)
            mode = gamemode()
        game(height, width, board, statistics)

def gamemode():
    mode = input("Play | Statistics | Quit\n")
    while 1 == 1:
        if mode == "Play" or mode == "play" or mode == "P" or mode == "p":
            return 0
        elif mode == "Statistics" or mode == "statistics" or mode == "S" or mode == "s":
            return -1
        elif mode == "Quit" or mode == "quit" or mode == "Q" or mode == "q":
            print("\nThanks for playing!\n")
            quit()
        else:
            print("Please enter a valid option\n")
            mode = input("Play | Statistics | Quit\n")
            

def print_stats(statistics):
    gamesPlayed = statistics[0] + statistics[1] + statistics[2]
    print("\n\nGames Played: %d" % (gamesPlayed))

    print("\n# Wins: %d" % (statistics[0]))
    if gamesPlayed != 0:
        winPercent1 = 100 * statistics[0] / (statistics[0] + statistics[1] + statistics[2])
        print("# Win Percentage: %d" % (winPercent1))

    print("\nO Wins: %s" % (statistics[1]))
    if gamesPlayed != 0:
        winPercent2 = 100 * statistics[1] / (statistics[0] + statistics[1] + statistics[2])
        print("O Win Percentage: %d" % (winPercent2))

    print("\nTied Games: %d" % (statistics[2]))

    print("\n")

def game(height, width, board, statistics):
    while 1 == 1:
        print("\n#'s turn:")
        print_board(height, width, board)
        choice = player_input(height, width, board)
        for i in range(1, height + 1):
            if board[(choice - 1) + (height - i) * width] == "-":
                board[(choice - 1) + (height - i) * width] = "#"
                break
        if win_condition(board) == True:
            print()
            print_board(height, width, board)
            print("# WINS!\n")
            statistics[0] = statistics[0] + 1
            return

        print("\nO's turn:")
        print_board(height, width, board)
        choice = player_input(height, width, board)
        for i in range(1, height + 1):
            if board[(choice - 1) + (height - i) * width] == "-":
                board[(choice - 1) + (height - i) * width] = "O"
                break
        if win_condition(board) == True:
            print("O WINS!")
            statistics[1] = statistics[1] + 1
            return

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
                
def win_condition(board):
    return False

main()