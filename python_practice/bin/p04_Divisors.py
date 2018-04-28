"""Create a program that asks the user for a number and then prints out a list of all the divisors of that number. (If you don’t know what a divisor is, it is a number that divides evenly into another number. For example, 13 is a divisor of 26 because 26 / 13 has no remainder.)
"""


def divisors_check(num_i):
    num1_i = num_i
    divisors = []
    while num1_i != 0:
        if num_i % num1_i == 0:
            divisors.append(num1_i)
        num1_i -= 1
    return divisors


def __init__():
    input_number = int(input("provide number: "))
    divisors_check(input_number)


