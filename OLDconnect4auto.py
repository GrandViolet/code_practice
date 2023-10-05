from random import choice

def main():
    print("\nWelcome to Connect Four")
    
    gameCount = 0
    maxGames = int(input())
    score = [0, 0, 0]

    menu(gameCount, maxGames, score)

def menu(gameCount, maxGames, score):
    x = 7
    y = 6
    gameCount = gameCount + 1
    
    gameState = []
    for p in range(y * x):
        gameState = gameState + ['-']
    while gameCount <= maxGames:
        print_board(gameCount, maxGames, score, x, y, gameState)
        game(gameCount, maxGames, score, x, y, gameState)
    quit()

def game(gameCount, maxGames, score, x, y, gameState):
    p1(gameCount, maxGames, score, x, y, gameState)
    p2(gameCount, maxGames, score, x, y, gameState)

def p1(gameCount, maxGames, score, x, y, gameState):
    print("\n@'s turn")
    currentColumn = int(choice(range(x))) + 1
    for i in range(y):
        if gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] == '-':
            gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] = '@'
            print_board(gameCount, maxGames, score, x, y, gameState)
            return
    p1(gameCount, maxGames, score, x, y, gameState)

def p2(gameCount, maxGames, score, x, y, gameState):
    print("\nX's turn")
    currentColumn = int(choice(range(x))) + 1
    for i in range(y):
        if gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] == '-':
            gameState[(x * y) - 1 - (x - currentColumn) - (x * i)] = 'X'
            print_board(gameCount, maxGames, score, x, y, gameState)
            return
    p2(gameCount, maxGames, score, x, y, gameState)

def print_board(gameCount, maxGames, score, x, y, gameState):
    outcome = 0
    for i in range(y):
        row = ""
        for p in range(x):
            row = row + gameState[p + (i * x)] + " "
        print(row)

    outcome = win_condition(gameCount, maxGames, score, x, y, gameState)
    outcome = draw_condition(gameCount, maxGames, score, gameState)
    return outcome

def win_condition(gameCount, maxGames, score, x, y, gameState):
    win = 4
    connect = []
    winCondition = 0
    outcome = 0

    for v in range(y):
        for p in range(x - win + 1):
            if gameState[p + (v * x)] != '-':
                winner = gameState[p + (v * x)]
                for i in range(win):
                    connect = connect + [gameState[i + p + (v * x)]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (horizontally)" % (winner))
                        if winner == "@":
                            score[0] = score[0] + 1
                        if winner == "X":
                            score[1] = score[1] + 1
                        retry(gameCount, maxGames, score)
                        outcome = 1
                        return outcome
                connect = []
                winCondition = 0
    
    for v in range(x):
        for p in range(y - win + 1):
            if gameState[v + (p * (y + 1))] != '-':
                winner = gameState[v + (p * (y + 1))]
                for i in range(win):
                    connect = connect + [gameState[(v + (i + p) * x)]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (vertically)" % (winner))
                        if winner == "@":
                            score[0] = score[0] + 1
                        if winner == "X":
                            score[1] = score[1] + 1
                        retry(gameCount, maxGames, score)
                        outcome = 1
                        return outcome
                connect = []
                winCondition = 0

    for v in range(y - win + 1):
        for p in range(x - win + 1):
            if gameState[p + (v * x)] != '-':
                winner = gameState[p + (v * x)]
                for i in range(win):
                    connect = connect + [gameState[(p + (i + v) * x) + i]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (diagonally right)" % (winner))
                        if winner == "@":
                            score[0] = score[0] + 1
                        if winner == "X":
                            score[1] = score[1] + 1
                        retry(gameCount, maxGames, score)
                        outcome = 1
                        return outcome
                connect = []
                winCondition = 0
    
    for v in range(y - win + 1):
        for p in range(x - win + 1):
            if gameState[(p + win - 1) + (v * x)] != '-':
                winner = gameState[(p + win - 1) + (v * x)]
                for i in range(win):
                    connect = connect + [gameState[((p + win - 1) + (i + v) * x) - i]]
                    if connect[i] == winner:
                        winCondition = winCondition + 1
                    if winCondition == win:
                        print("\n%s WINS! (diagonally left)" % (winner))
                        if winner == "@":
                            score[0] = score[0] + 1
                        if winner == "X":
                            score[1] = score[1] + 1
                        retry(gameCount, maxGames, score)
                        outcome = 1
                        return outcome
                connect = []
                winCondition = 0

def draw_condition(gameCount, maxGames, score, gameState):
    drawCondition = 0
    outcome = 0
    for i in range(len(gameState)):
        if gameState[i] == '-':
            drawCondition = drawCondition + 1
    if drawCondition == 0:
        print("\nIt's a tie!")
        score[2] = score[2] + 1
        retry(gameCount, maxGames, score)
        outcome = 1
        return outcome

def retry(gameCount, maxGames, score):
    print("%d / %d" % (gameCount, maxGames))
    print(score)

main()