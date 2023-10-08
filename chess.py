from random import choice

def main():
    print("\nWelcome to Chess!\n")

    statistics = [0, 0, 0]

    while 1 == 1:
        mode = gamemode()

        if mode == -2:
            break
      
        elif mode == -1:
            stats(statistics)

        elif mode == 3:
            auto_controller(statistics, mode)
      
        else:
            game(statistics, mode)
    
    print("Thank you for playing!\n")

def gamemode():
    while 1 == 1:
        mode = input("Multiplayer | Computer | Auto | Statistics | Quit\n")
        if mode == "Multiplayer" or mode == "multiplayer" or mode == "M" or mode == "m":
            return 0
        
        if mode == "Computer" or mode == "computer" or mode == "C" or mode == "c":
            color = input("Would you like to play white or black?\n")
            if color == "White" or color == "white" or color == "W" or color == "w":
                return 1
            elif color == "Black" or color == "black" or color == "B" or color == "b":
                return 2
            
        if mode == "Auto" or mode == "auto" or mode == "A" or mode == "a":
            return 3
        
        if mode == "Statistics" or mode == "statistics" or mode == "S" or mode == "s":
            return -1
        
        if mode == "Quit" or mode == "quit" or mode == "Q" or mode == "q":
            return -2
        
        print("Please enter a valid option\n")

def stats(statistics):
    gamesPlayed = statistics[0] + statistics[1] + statistics[2]
    print("\n\nGames Played: %d" % (gamesPlayed))

    print("\nWhite Wins: %d" % (statistics[0]))
    if gamesPlayed != 0:
        winPercent1 = 100 * statistics[0] / (statistics[0] + statistics[1] + statistics[2])
        print("White Win Percentage: %.2f" % (winPercent1))

    print("\nBlack Wins: %d" % (statistics[1]))
    if gamesPlayed != 0:
        winPercent2 = 100 * statistics[1] / (statistics[0] + statistics[1] + statistics[2])
        print("Black Win Percentage: %.2f" % (winPercent2))

    print("\nDraws: %d" % (statistics[2]))
    if gamesPlayed != 0:
        tiePercent = 100 * statistics[2] / (statistics[0] + statistics[1] + statistics[2])
        print("Draw Percentage: %.2f" % (tiePercent))

    print("\n")

def auto_controller(statistics, mode):
    while 1 == 1:
        digitCount = 0

        games = input("How many games would you like it to play?\n")
        for digit in games:
            if ord(digit) >= 48 and ord(digit) <= 57:
                digitCount = digitCount + 1
            if digitCount == len(games):
                for i in range(int(games)):
                    game(statistics, mode)
                stats(statistics)
                return()
        print("Please enter a valid number")


def game(statistics, mode):
    board = board_initializer()
    round = 0

    while 1 == 1:
        if round%2 == 0:
            print("\nWhite's turn:")
        if round%2 == 1:
            print("\nBlack's turn:")
        
        print_board(board)
        
        selection = select_square(board, round)

        if board[selection[0]][selection[1]] == "r" or board[selection[0]][selection[1]] == "R":
            rook_controller(board, selection)
        elif board[selection[0]][selection[1]] == "h" or board[selection[0]][selection[1]] == "H":
            knight_controller(board, selection)
        elif board[selection[0]][selection[1]] == "b" or board[selection[0]][selection[1]] == "B":
            bishop_controller(board, selection)
        elif board[selection[0]][selection[1]] == "q" or board[selection[0]][selection[1]] == "Q":
            queen_controller(board, selection)
        elif board[selection[0]][selection[1]] == "k" or board[selection[0]][selection[1]] == "K":
            king_controller(board, selection)
        elif board[selection[0]][selection[1]] == "p" or board[selection[0]][selection[1]] == "P":
            pawn_controller(board, selection)

        round = round + 1

def board_initializer():
    board = []
    for i in range(8):
        board.append("-")
    board = [board] * 8

    board[0] = ["R", "H", "B", "Q", "K", "B", "H", "R"]
    board[1] = ["P", "P", "P", "P", "P", "P", "P", "P"]
    board[6] = ["p", "p", "p", "p", "p", "p", "p", "p"]
    board[7] = ["r", "h", "b", "q", "k", "b", "h", "r"]

    #board[7] = ["-", "-", "-", "r", "-", "-", "-", "-"]

    return board

def print_board(board):
    for i in range(8):
        row = ""
        for j in range(8):
            row = row + str(board[i][j]) + " "
        print(row)
    print()

def select_square(board, round):
    while 1 == 1:
        square = input("Select a piece to move\n")
        if len(square) == 2:
            if ord(square[0]) >= 65 and ord(square[0]) <= 72:
                column = ord(square[0]) - 65
            elif ord(square[0]) >= 97 and ord(square[0]) <= 104:
                column = ord(square[0]) - 97
            else:
                column = -1
            if column >= 0 and column <= 7:
                if ord(square[1]) >= 49 and ord(square[1]) <= 56:
                    row = 7 - (ord(square[1]) - 49)
                else:
                    row = -1
                if row >= 0 and row <= 7:
                    if round%2 == 0:
                        validPieces = ["r", "h", "b", "q", "k", "p"]
                    if round%2 == 1:
                        validPieces = ["R", "H", "B", "Q", "K", "P"]
                    for col in validPieces:
                        if board[row][column] == col:
                            return [row, column]
                    print("Please select a square with one of your pieces on it\n")
                else:
                    print("Please select a valid row (1-8)\n")
            else:
                print("Please select a valid column (A-H)\n")
        else:
            print("Please select a valid square\n")

def cpu_select_square(board, round):
    while 1 == 1:
        column = choice(range(8))
        row = choice(range(8))
        if round%2 == 0:
            validPieces = ["r", "h", "b", "q", "k", "p"]
        if round%2 == 1:
            validPieces = ["R", "H", "B", "Q", "K", "P"]
        for col in validPieces:
            if board[row][column] == col:
                return [row, column]


def rook_controller(board, selection):
    return

def knight_controller(board, selection):
    return

def bishop_controller(board, selection):
    return

def queen_controller(board, selection):
    return

def king_controller(board, selection):
    return

def pawn_controller(board, selection):
    return

main()