"""
Take two lists, say for example these two:

  a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
  b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

and write a program that returns a list that contains only the elements that are common between the lists (without duplicates). Make sure your program works on two lists of different sizes.

Extras:

    Randomly generate two lists to test this
    Write this in one line of Python (don’t worry if you can’t figure this out at this point - we’ll get to it soon)

"""
from sys import exit
from random import randint


def lists_input(user_opt):

    if user_opt == 'r':
        global a, b
        a = []
        b = []
        rad1 = randint(0, 10)
        rad2 = randint(0, 10)
        for i in range(0, rad1):
            a.append(randint(0, 100))
        for i in range(0, rad2):
            b.append(randint(0, 100))
    elif user_opt == 'd':
        a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    else:
        print("incorrect input")
        exit(1)


print('generate lists randomly or use default lists?(r/d): ')
usr1 = input()

lists_input(usr1)

print("your lists will be following:")
print("a = ", a)
print("b = ", b)

c = []
for check_a in a:
    for check_b in b:
        if check_b == check_a:
            if check_b not in c:
                c.append(check_b)
print("Result: ", c)
