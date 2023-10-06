from random import choice

def main():
    houses = 6
    startingStones = 4

    print("\nWelcome to Mancala!")

    statistics = [0, 0, 0]
    while 1 == 1:
        mode = gamemode()
        while mode == -1:
            stats(statistics)
            mode = gamemode()
        if mode == 2:
                games = int(input("How many games would you like it to play?\n"))
                gameCount = 0
                while gameCount < games:
                    game(statistics, mode, houses, startingStones)
                    gameCount = gameCount + 1
                stats(statistics)
        if mode == 0 or mode == 1:
            game(statistics, mode, houses, startingStones)

def gamemode():
    mode = input("Multiplayer | Computer | Automatic | Statistics | Quit\n")
    while 1 == 1:
        if mode == "Multiplayer" or mode == "multiplayer" or mode == "M" or mode == "m":
            return 0
        elif mode == "Computer" or mode == "computer" or mode == "C" or mode == "c":
            return 1
        elif mode == "Automatic" or mode == "automatic" or mode == "A" or mode == "a":
            return 2
        elif mode == "Statistics" or mode == "statistics" or mode == "S" or mode == "s":
            return -1
        elif mode == "Quit" or mode == "quit" or mode == "Q" or mode == "q":
            print("\nThanks for playing!\n")
            quit()
        else:
            print("Please enter a valid option\n")
            mode = input("Multiplayer | Computer | Automatic | Statistics | Quit\n")

def stats(statistics):
    gamesPlayed = statistics[0] + statistics[1] + statistics[2]
    print("\n\nGames Played: %d" % (gamesPlayed))

    print("\nPlayer 1 Wins: %d" % (statistics[0]))
    if gamesPlayed != 0:
        winPercent1 = 100 * statistics[0] / (statistics[0] + statistics[1] + statistics[2])
        print("Player 1 Win Percentage: %.2f" % (winPercent1))

    print("\nPlayer 2 Wins: %d" % (statistics[1]))
    if gamesPlayed != 0:
        winPercent2 = 100 * statistics[1] / (statistics[0] + statistics[1] + statistics[2])
        print("Player 2 Win Percentage: %.2f" % (winPercent2))

    print("\nTied Games: %d" % (statistics[2]))
    if gamesPlayed != 0:
        tiePercent = 100 * statistics[2] / (statistics[0] + statistics[1] + statistics[2])
        print("Tie Percentage: %.2f" % (tiePercent))

    print("\n")

def game(statistics, mode, houses, startingStones):
    board = []
    for i in range(houses):
        board.append(startingStones)
    board.append(0)
    board = board * 2

    round = 0

    while 1 == 1:
        bonusTurn = False

        if round%2 == 0:
            print("\nPlayer 1:")
        if round%2 == 1:
            print("\nPlayer 2:")
        
        print_board(board, houses)

        if mode == 0 or (mode == 1 and round%2 == 0):
            house = player_input(board, houses)
        elif (mode == 1 and round%2 == 1) or mode == 2:
            house = cpu_input(board, houses)

        stones = board[house - 1]

        if (stones + (house - 1))%(len(board) - 1) == houses:
            bonusTurn = True

        board[house - 1] = 0

        stone_distribution(board, stones, house, houses)
        if game_end(board, houses) == True:
            break

        if bonusTurn == False:
            round = round + 1
            reverse_board(board)
    
    game_over(round, board, houses, statistics)
      
def print_board(board, houses):
    row1 = " " * (len(str(board[len(board) - 1])) + 2)
    for i in range(houses):
        row1 = row1 + str(board[(len(board)) - (2 + i)]) + " "
    print(row1)

    row2 = " " * (len(str(board[len(board) - 1])) + 2)
    for i in range(houses):
        row2 = row2 + str(board[i]) + " "
    
    rowLength = max(len(row1), len(row2))

    print(str(board[len(board) - 1]) + " " * rowLength + str(board[houses]))

    print(row2)

    print()

def player_input(board, houses):
    house = int(input())
    while (house < 1 or house > houses) or board[house - 1] == 0:
        if not (house < 1 or house > houses):
            print("Please select a house with stones")
            print_board(board, houses)
        else:
            print("Please select a valid house")
        house = int(input())
    return house

def cpu_input(board, houses):
    house = choice(range(houses)) + 1
    while (house < 1 or house > houses) or board[house - 1] == 0:
        house = choice(range(houses)) + 1
    print(house)
    return house

def stone_distribution(board, stones, house, houses):
    while stones > len(board) - 1:
        for i in range(len(board) - 1):
            board[i] = board[i] + 1
            stones = stones - 1
    
    for i in range(len(board) - house - 1):
        board[house + i] = board[house + i] + 1
        stones = stones - 1
        if stones == 0:
            capture(board, house, i, houses)
            break
    
    i = 0
    while stones > 0:
        board[i] = board[i] + 1
        stones = stones - 1
        i = i + 1

def capture(board, house, i, houses):
    if board[house + i] == 1:
        if board[len(board) - 2 - (house + i)] != 0:
            if house + i < houses:
                board[houses] = board[houses] + board[len(board) - 2 - (house + i)] + 1
                board[house + i] = 0
                board[len(board) - 2 - (house + i)] = 0

def reverse_board(board):
    for i in range(len(board) // 2):
        board.append(board[i])
    del board[0:len(board) // 3]

def game_end(board, houses):
    end_condition = 0
    for i in range(houses):
        if board[i] == 0:
            end_condition = end_condition + 1
    if end_condition == houses:
        return True
    
    end_condition = 0
    for i in range(houses):
        if board[i + houses + 1] == 0:
            end_condition = end_condition + 1
    if end_condition == houses:
        return True
    
    return False

def game_over(round, board, houses, statistics):
    print()
    print_board(board, houses)
    if board[houses] == board[len(board) - 1]:
        print("It's a tie")
        statistics[2] = statistics[2] + 1
    if round%2 == 0:
        if board[houses] > board[len(board) - 1]:
            print("Player 1 wins")
            statistics[0] = statistics[0] + 1
        elif board[houses] < board[len(board) - 1]:
            print("Player 2 wins")
            statistics[1] = statistics[1] + 1
    elif round%2 == 1:
        if board[houses] > board[len(board) - 1]:
            print("Player 2 wins")
            statistics[1] = statistics[1] + 1
        elif board[houses] < board[len(board) - 1]:
            print("Player 1 wins")
            statistics[0] = statistics[0] + 1

main()