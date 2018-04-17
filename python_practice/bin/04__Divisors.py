"""Create a program that asks the user for a number and then prints out a list of all the divisors of that number. (If you don’t know what a divisor is, it is a number that divides evenly into another number. For example, 13 is a divisor of 26 because 26 / 13 has no remainder.)
"""
num = int(input("provide number: "))
num1 = num
a = []


while num1 != 0:
    if num % num1 == 0:
        a.append(num1)
    num1 -= 1
print(a)
