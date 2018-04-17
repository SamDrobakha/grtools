"""
Create a program that asks the user to enter their name and their age. Print out a message addressed to them that tells them the year that they will turn 100 years old.

Extras:

    Add on to the previous program by asking the user for another number and printing out that many copies of the previous message. (Hint: order of operations exists in Python)
    Print out that many copies of the previous message on separate lines. (Hint: the string "\n is the same as pressing the ENTER button)
"""
import datetime


def f_age100y(name_i, age_i, messages_count_i):
    current = datetime.date.today()
    age100y = current.year - age_i + 100
    for i in range(0, messages_count_i):
        print(name_i, age100y)


name = input('Enter your name: ')
age = int(input('Enter your age: '))
messages_count = int(input('Enter how many times to repeat result message: '))

f_age100y(name, age, messages_count)
