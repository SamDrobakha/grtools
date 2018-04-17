"""
Ask the user for a number. Depending on whether the number is even or odd, print out an appropriate message to the user. Hint: how does an even / odd number react differently when divided by 2?

Extras:

    If the number is a multiple of 4, print out a different message.
    Ask the user for two numbers: one number to check (call it num) and one number to divide by (check). If check divides evenly into num, tell that to the user. If not, print a different appropriate message.
"""

check = int(input("Provide 'check' number: "))
num = int(input("Provide 'num' number: "))

if num % 4 ==0:
    print("your number is a multiple of 4")
elif num % 2 == 0:
    print("your 'num' number is even")
else:
    print("your 'num' number is odd")

if check % num == 0:
    print("check divide num is int value (divides evently)")
else:
    print("check divide num is float value (not divides evently)")
