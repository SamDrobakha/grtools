"""
Ask the user for a number and determine whether the number is prime or not. (For those who have forgotten, a prime number is a number that has no divisors.). You can (and should!) use your answer to Exercise 4 to help you. Take this opportunity to practice using functions, described below.
# 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,

THIS will calculate primes till 2 in power n
"""

import p04_Divisors as Div


def __init__():
    print("Give 2 in power n to which we will look for primes")
    print('(example 2**4 will calculate all primes in range 0..16): ')
    input_n_power = int(input())
    res = check_if_prime_npower(input_n_power)
    print('primes list in range 0..', 2**input_n_power, ' : ', res)


def check_if_prime_npower(input_n_power_i):
    primes = list()
    area_m = list(range(0, 2**input_n_power_i))

    for i in range(0, len(area_m)):
        check_area_m = (Div.divisors_check(area_m[i]))
        if len(check_area_m) > 2:
            continue
        else:
            print(area_m[i])
            primes.append(area_m[i])

    return primes


__init__()
