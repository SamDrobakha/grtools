"""
Write a program that takes a list of numbers (for example, a = [5, 10, 15, 20, 25]) and makes a new list of only the first and last elements of the given list. For practice, write this code inside a function.
"""


def fist_last_list_element(list_i):
    b = []
    c = len(list_i)
    b.append(list_i[0])
    b.append(list_i[c-1])
    return b


def __init__():
    a = [5, 10, 15, 20, 25, 30, 35]
    res = fist_last_list_element(a)
    print(res)


__init__()
