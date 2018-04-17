"""
Generate a random number between 1 and 9 (including 1 and 9). Ask the user to guess the number, then tell them whether they guessed too low, too high, or exactly right. (Hint: remember to use the user input lessons from the very first exercise)

Extras:

    Keep the game going until the user types “exit”
    Keep track of how many guesses the user has taken, and when the game ends, print this out.
"""

from random import randint
from sys import exit


def guessing_validat(inp1, gen):
    if inp1 > gen:
        print("User value is bigger")
        fl = False
    elif inp1 < gen:
        print("User value is lover")
        fl = False
    else:
        print("Yes, its right ", inp1, " is equal ", gen)
        fl = True
    return fl


def set_secret():
    gen = randint(1, 9)
    return gen


def guessing_main():
    print("guessing game. for exit type 'exit'")
    secret = set_secret()
    i = 0
    while True:
        try:
            inp1 = input("Provide your number from 1 to 9 incl. - we'll see if you'll guess 1-9: ")
            inp11 = int(inp1)
            if type(inp11) is int:
                if inp11 < 1:
                    print("your number <1")
                    continue
                elif inp11 > 9:
                    print("your number >9")
                    continue
                else:
                    fl = guessing_validat(inp11, secret)
                    if fl is True:
                        a = input('new game?(y/n) ')
                        if a == 'y':
                            secret = set_secret()
                            i += 1
                            continue
                        elif a == 'n':
                            i += 1
                            print('games played: ', i)
                            exit()
                        else:
                            exit(1)
                    else:
                        continue
                    continue
        except ValueError:
            if type(inp1) is str:
                if inp1 == 'exit':
                    exit(0)
                else:
                    print('I didnt understand')
                continue
        else:
            continue


guessing_main()

