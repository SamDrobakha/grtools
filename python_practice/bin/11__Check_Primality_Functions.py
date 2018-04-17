"""
Ask the user for a number and determine whether the number is prime or not. (For those who have forgotten, a prime number is a number that has no divisors.). You can (and should!) use your answer to Exercise 4 to help you. Take this opportunity to practice using functions, described below.
"""
primes = []
prime = True

# test = int(input('give number(>1): '))
for test in range(2, 100):
    for test_WE in range(2, test-1):
        if test % test_WE == 0:
            prime = False
            break
    if prime is True:
        primes.append(test)
print(primes)
"""    
    test_WE = test
    while test_WE != 2:
        if test % test_WE - (test_WE - 2) == 0:
            prime = False
            break
        else:
            prime = True
        test_WE = test_WE - 1
    if prime is True:
        primes.append(test)

print(primes)
"""
# 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,