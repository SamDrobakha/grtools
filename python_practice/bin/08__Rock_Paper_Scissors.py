"""
Make a two-player Rock-Paper-Scissors game. (Hint: Ask for player plays (using input), compare them, print out a message of congratulations to the winner, and ask if the players want to start a new game)

Remember the rules:
    Rock beats scissors
    Scissors beats paper
    Paper beats rock

"""


def rps_game_engine(play1, play2):
    draw = 0
    p1_win = 1
    p2_win = 2
    logic = {
        ("rock", "paper"): p2_win,
        ("rock", "scissors"): p1_win,
        ("rock", "rock"): draw,
        ("paper", "rock"): p1_win,
        ("paper", "scissors"): p2_win,
        ("paper", "paper"): draw,
        ("scissors", "rock"): p2_win,
        ("scissors", "paper"): p1_win,
        ("scissors", "scissors"): draw
    }
    return logic[(play1, play2)]


def rps_results_decision(result):
    # result = rps_game_engine(inp1, inp2)
    if result == 2:
        print("Player 2 win!")
    elif result == 1:
        print("Player 1 win!")
    else:
        print("Draw!")


def game_main():
    while True:
        inp1 = str(input("Player 1: rock, paper or scissors? "))
        inp2 = str(input("Player 2: rock, paper or scissors? "))

        result = rps_game_engine(inp1, inp2)
        rps_results_decision(result)
        a = input("Would you like to start new game(y/n)? ")
        if a == "y":
            continue
        else:
            break


game_main()
