from random import choice

def main():
    maxAttempts = 10
    digits = 6

    print("\nWelcome to Decode the Code!")
    menu(maxAttempts, digits)

def menu(maxAttempts, digits):
    gamemode = input("\nEasy or hard? ")
    if gamemode == "easy" or gamemode == "Easy" or gamemode == "e" or gamemode == "E":
        difficulty = 4
    elif gamemode == "hard" or gamemode == "Hard" or gamemode == "h" or gamemode == "H":
        difficulty = 5
    elif gamemode == "custom" or gamemode == "Custom" or gamemode == "c" or gamemode == "C":
        difficulty = int(input())
    else:
        print("\nPlease enter a valid gamemode")
        menu(maxAttempts, digits)

    solution = ""
    for i in range(difficulty):
        solution = solution + str(choice(range(digits)) + 1)
    #print(solution)

    attempts = 1
    previousGuesses = ""

    printBoard(solution, "", 0, 0, attempts, maxAttempts, previousGuesses, "")
    game(solution, attempts, maxAttempts, previousGuesses)

    if input("Would you like to play again? (y/n) ") == "y":
        menu(maxAttempts, digits)
    else:
        print("\nThanks for playing!\n")
        quit()

def game(solution, attempts, maxAttempts, previousGuesses):

    blackCount = 0
    whiteCount = 0
    
    guess = input("\n")
    if len(guess) != len(solution):
        print("Please enter a guess with %d digits" % (len(solution)))
        game(solution, attempts, maxAttempts, previousGuesses)

    attempts = attempts + 1

    guessList = list(guess)
    solutionList = list(solution)

    for i in range(len(solution)):
        if guessList[i] == solutionList[i]:
            blackCount = blackCount + 1
            guessList[i] = -1
            solutionList[i] = -2
    
    for i in range(len(solution)):
        for j in range(len(solution)):
            if guessList[i] == solutionList[j]:
                whiteCount = whiteCount + 1
                guessList[i] = -1
                solutionList[j] = -2

    correctGuesses = 0
    for i in range(len(solution)):
        if guess[i] == solution[i]:
            correctGuesses = correctGuesses + 1
    
    previousGuesses = printBoard(guess, solution, blackCount, whiteCount, attempts, maxAttempts, previousGuesses, correctGuesses)

    if correctGuesses == len(solution):
        print("You Win!")
        return
    elif attempts > maxAttempts:
        print("Game Over!")
        return
    else:
        game(solution, attempts, maxAttempts, previousGuesses)

def printBoard(guess, solution, blackCount, whiteCount, attempts, maxAttempts, previousGuesses, correctGuesses):
    if attempts <= maxAttempts and correctGuesses != len(solution):
        print("\n" + "?" * len(guess))
    else:
        print("\n" + solution)
    
    for i in range(maxAttempts - attempts + 1):
        print("-" * len(guess))

    if attempts != 1:
        guess = guess + "   B: %s, W: %s" % (blackCount, whiteCount)
        print(guess)

    print(previousGuesses)
    previousGuesses = guess + "\n" + previousGuesses
    return previousGuesses

main()