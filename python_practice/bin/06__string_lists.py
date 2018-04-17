"""
Ask the user for a string and print out whether this string is a palindrome or not. (A palindrome is a string that reads the same forwards and backwards.)
"""

while True:
    try:
        usr_input1 = str(input("Please provide a string and we'll verify if its palindrome: "))
    except ValueError:
        print("Sorry, I didn't understand that.")
        #better try again... Return to the start of the loop
        continue
    else:
        #input was successfully parsed!
        #we're ready to exit the loop.
        break
usr_input1_len = len(usr_input1) - 1
fl = bool
for i in range(0, usr_input1_len):
    if usr_input1[i] == usr_input1[usr_input1_len - i]:
        fl = True
        continue
    else:
        print("It's not palindrome")
        break

if fl is True:
    print("It is palindrome")
