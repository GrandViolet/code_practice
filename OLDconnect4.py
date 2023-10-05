from random import choice

def main():
    print("\nWelcome to Connect Four")
    menu()

def menu():
    x = 17
    y = 6
    
    mode = input("\nSingleplayer or multiplayer? ")
    if mode == "singleplayer" or mode == "Singleplayer" or mode == "s" or mode == "S":
        mode = 0
    elif mode == "multiplayer" or mode == "Multiplayer" or mode == "m" or mode == "M":
        mode = 1
    else:
        print("Please enter a valid gamemode")
        menu()

    gameState = []
    for p in range(y * x):
        gameState = gameState + ['-']

    print("\n@'s turn")
    print_board(x, y, gameState)
    game(mode, x, y, gameState)

def game(mode, x, y, gameState):
    currentColumn = int(input("Column: "))
    if currentColumn > x or currentColumn <= 0:
        print("\nPlease select a valid column")
        print("\n@'s turn")
        print_board(x, y, gameState)
        game(mode, x, y, gameState)
    
    for i in range(y):
        if gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] == '-':
            gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] = '@'
            print("\nX's turn:")
            print_board(x, y, gameState)
            if mode == 0:
                cpu(mode, x, y, gameState)
            if mode == 1:
                game2(mode, x, y, gameState)
    print("\nColumn full!")
    print("\n@'s turn")
    print_board(x, y, gameState)
    game(mode, x, y, gameState)

def game2(mode, x, y, gameState):
    currentColumn = int(input("Column: "))
    if currentColumn > x or currentColumn <= 0:
        print("\nPlease select a valid column")
        print("\nX's turn:")
        print_board(x, y, gameState)
        game(mode, x, y, gameState)
    
    for i in range(y):
        if gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] == '-':
            gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] = 'X'
            print("\n@'s turn:")
            print_board(x, y, gameState)
            game(mode, x, y, gameState)
    print("\nColumn full!")
    print("\nX's turn:")
    print_board(x, y, gameState)
    game2(mode, x, y, gameState)

def print_board(x, y, state):
    for i in range(y):
        row = ""
        for p in range(x):
            row = row + state[p + (i * x)] + " "
        print(row)
    
    win_condition(x, y, state)
    draw_condition(state)

def cpu(mode, x, y, gameState):
    currentColumn = int(choice(range(x))) + 1
    for i in range(y):
        if gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] == '-':
            gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] = 'X'
            print("\n@'s turn:")
            print_board(x, y, gameState)
            game(mode, x, y, gameState)
    cpu(mode, x, y, gameState)

def win_condition(x, y, state):
    win = 4
    connect = []
    winCondition = 0

    for v in range(y):
        for p in range(x - win + 1):
            if state[p + (v * x)] != '-':
                winner = state[p + (v * x)]
                for i in range(win):
                    connect = connect + [state[i + p + (v * x)]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (horizontally)" % (winner))
                        retry()
                connect = []
                winCondition = 0
    
    for v in range(x):
        for p in range(y - win + 1):
            if state[v + (p * (y + 1))] != '-':
                winner = state[v + (p * (y + 1))]
                for i in range(win):
                    connect = connect + [state[(v + (i + p) * x)]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (vertically)" % (winner))
                        retry()
                connect = []
                winCondition = 0

    for v in range(y - win + 1):
        for p in range(x - win + 1):
            if state[p + (v * x)] != '-':
                winner = state[p + (v * x)]
                for i in range(win):
                    connect = connect + [state[(p + (i + v) * x) + i]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (diagonally right)" % (winner))
                        retry()
                connect = []
                winCondition = 0
    
    for v in range(y - win + 1):
        for p in range(x - win + 1):
            if state[(p + win - 1) + (v * x)] != '-':
                winner = state[(p + win - 1) + (v * x)]
                for i in range(win):
                    connect = connect + [state[((p + win - 1) + (i + v) * x) - i]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (diagonally left)" % (winner))
                        retry()
                connect = []
                winCondition = 0

def retry():
    if input("Would you like to play again? (y/n) ") == "y":
        menu()
    else:
        print("Thanks for playing!")
        quit()

def draw_condition(state):
    drawCondition = 0
    for i in range(len(state)):
        if state[i] == '-':
            drawCondition = drawCondition + 1
    if drawCondition == 0:
        print("\nIt's a tie!")
        retry()

main()