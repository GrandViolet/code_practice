from random import choice

def main():
    symbols = 6
    maxAttempts = 10

    print("\nWelcome to Decode the Code!")
    print("Developed by Square Lion and Grand Violet\n")

    statistics = [0, 0, 0, 0]
    
    while 1 == 1:
        mode = gamemode(statistics)
        while mode == -1:
            stats(statistics)
            mode = gamemode(statistics)
        game(symbols, mode, maxAttempts, statistics)

def gamemode(statistics):
    while 1 == 1:
        mode = input("Normal | Hard | Statistics | Quit\n")
        if mode == "normal" or mode == "Normal" or mode == "n" or mode == "N":
            statistics[0] = statistics[0] + 1
            return 4
        if mode == "hard" or mode == "Hard" or mode == "h" or mode == "H":
            statistics[2] = statistics[2] + 1
            return 5
        if mode == "custom" or mode == "Custom" or mode == "c" or mode == "C":
            return int(input())
        if mode == "statistics" or mode == "Statistics" or mode == "s" or mode == "S":
            return -1
        if mode == "quit" or mode == "Quit" or mode == "q" or mode == "Q":
            print("\nThanks for playing!\n")
            quit()
        print("Please enter a valid option")

def stats(statistics):
    print("\n\nNormal Games Played: %d" % (statistics[0]))
    print("Normal Games Won: %d" % (statistics[1]))
    if statistics[0] != 0:
        nWinPercentage = 100 * statistics[1] // statistics[0]
        print("Normal Win Percentage: %d" % (nWinPercentage))

    print("\nHard Games Played: %d" % (statistics[2]))
    print("Hard Games Won: %d" % (statistics[3]))
    if statistics[2] != 0:
        hWinPercentage = 100 * statistics[3] // statistics[2]
        print("Hard Win Percentage: %d" % (hWinPercentage))
    
    tGamesPlayed = statistics[0] + statistics[2]
    tGamesWon = statistics[1] + statistics[3]
    print("\nTotal Games Played: %d" % (tGamesPlayed))
    print("Total Games Won: %d" % (tGamesWon))
    if tGamesPlayed != 0:
        tWinPercentage = 100 * tGamesWon // tGamesPlayed
        print("Total Win Percentage: %d" % (tWinPercentage))
    
    print("\n")

def game(symbols, length, maxAttempts, statistics):
    attemptCount = 0
    playerGuess = ""
    state = []
    pegs = []

    solution = answer(symbols, length)
    #print(solution)

    print_board(solution, playerGuess, length, maxAttempts, attemptCount, state, pegs)

    while solution != playerGuess and maxAttempts > attemptCount:
        attemptCount = attemptCount + 1
        playerGuess = guess(length)
        print()
        state.append(playerGuess)
        pegs.append(black_pegs(solution, playerGuess))
        pegs.append(white_pegs(solution, playerGuess) - black_pegs(solution, playerGuess))
        print_board(solution, playerGuess, length, maxAttempts, attemptCount, state, pegs)

    if solution == playerGuess:
        print("You win!")
        if length == 4:
            statistics[1] = statistics[1] + 1
        if length == 5:
            statistics[3] = statistics[3] + 1
    else:
        print("You lose!")

def answer(symbols, length):
    solution = ""
    for i in range(length):
        solution = solution + str(choice(range(symbols)) + 1)
    return solution

def guess(length):
    playerGuess = input()
    while len(playerGuess) != length:
        print("Please enter a guess of length %d" % (length))
        playerGuess = input()
    return playerGuess

def black_pegs(solution, playerGuess):
    blackCount = 0
    for i in range(len(solution)):
        if solution[i] == playerGuess[i]:
            blackCount = blackCount + 1
    return blackCount

def white_pegs(solution, playerGuess):
    whiteCount = 0
    guessList = list(playerGuess)
    solutionList = list(solution)

    for i in range(len(solution)):
        for j in range(len(solution)):
            if guessList[i] == solutionList[j]:
                whiteCount = whiteCount + 1
                guessList[i] = "a"
                solutionList[j] = "b"
    return whiteCount

def print_board(solution, playerGuess, length, maxAttempts, attemptCount, state, pegs):
    print()
    if solution != playerGuess and maxAttempts > attemptCount:
        print("?" * length)
    else:
        print(solution)

    for i in range(maxAttempts - attemptCount):
        print("-" * length)
    for i in range(attemptCount - 1, -1, -1):
        print("%s   B: %d  W: %d" % (state[i], pegs[2 * i], pegs[2 * i + 1]))
    print()

main()