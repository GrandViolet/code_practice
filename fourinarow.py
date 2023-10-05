from random import choice

def main():
    height = 6
    width = 7
    winCondition = 4

    print("\nWelcome to Four in a Row!")

    board = []
    for i in range(height * width):
        board.append("-")

    while 1 == 1:
        print("\n#'s turn:")
        print_board(height, width, board)
        choice = player_input(height, width, board)
        for i in range(1, height + 1):
            if board[(choice - 1) + (height - i) * width] == "-":
                board[(choice - 1) + (height - i) * width] = "#"
                break

        print("\nO's turn:")
        print_board(height, width, board)
        choice = player_input(height, width, board)
        for i in range(1, height + 1):
            if board[(choice - 1) + (height - i) * width] == "-":
                board[(choice - 1) + (height - i) * width] = "O"
                break

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
                    
        
            
                
main()