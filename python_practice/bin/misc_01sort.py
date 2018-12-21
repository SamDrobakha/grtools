"""
I heard someone asked candidate on interview to write program which sorts 0 and 1 from provided list.
I want to write the same as python exercise
"""

#sample list
sample = [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1]
b0 = []
c1 = []
d1 = []


for i in range(0, len(sample)):
    if sample[i] is 0:
        b0.append(sample[i])
    elif sample[i] is 1:
        c1.append(sample[i])
    else:
        print("list contain illegal objects, exiting")
        break

#result
print("original list length is: ", len(sample))
print("zeros count: ", len(b0), " ones count: ", len(c1))
print(sample)
print(b0)
print(c1)
