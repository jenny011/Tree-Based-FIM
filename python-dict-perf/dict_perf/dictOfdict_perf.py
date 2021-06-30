import random
from time import time
import numpy as np
import matplotlib.pyplot as plt

# size = 1000
# x = [i for i in range(1, size + 1)]
# insert = []
# lookup = []
# d = {}
# for i in x:
#     insert_s = time()
#     d[i] = str(i)
#     insert_e = time()
#     index = random.randint(1,size)
#     lookup_s = time()
#     d.get(index, None)
#     lookup_e = time()
#     insert.append(insert_e - insert_s)
#     lookup.append(lookup_e - lookup_s)

# plt.plot(x, insert, linestyle='-')
# plt.plot(x, lookup, linestyle='-')
# plt.show()
#
# print(max(insert), min(insert), np.mean(insert))

total_insert = []
total_lookup = []
x = [i for i in range(100000, 5000000, 500000)]

for i in x:
    insert = []
    lookup = []
    mainD = {}
    d = {}
    for j in range(0, i):
        d[j] = j
        if len(d) >= 50000:
            mainD[j] = d
            d = {}
    keys = sorted(mainD.keys())
    for k in range(1000):
        index = random.randint(0, i-1)
        lookup_s = time()
        if index > keys[-1]:
            ret = None
        for key in keys:
            if index <= key:
                ret = mainD[key][index]
                break
        lookup_e = time()
        lookup.append(lookup_e - lookup_s)
    # for k in range(1000):
    #     index = random.randint(i, i+100000)
    #     insert_s = time()
    #     d[index] = index
    #     insert_e = time()
    #     insert.append(insert_e - insert_s)
    # total_insert.append(sum(insert))
    total_lookup.append(sum(lookup))

# plt.plot(x, total_insert, linestyle='-', color='red')
plt.plot(x, total_lookup, linestyle='-', color='blue')
plt.show()

# print(max(insert), min(insert), np.mean(insert))
