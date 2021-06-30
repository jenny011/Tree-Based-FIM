import os
import sys
import random
from time import time
import numpy as np
import csv

def outputToCSV(op, x, means, errs):
    with open(os.path.join(os. getcwd(), "results", op + ".csv"), mode = 'w') as f:
        writer = csv.writer(f)
        for i in range(len(means)):
            writer.writerow([x[i], means[i], errs[i]])


def readDataset(fpath):
    dataset = []
    with open(fpath, 'r') as f:
        for line in f:
            dataset.append(line.rstrip())
    return dataset

def dictFromDataset():
    pass

def simpleDict(n):
    d = {}
    while len(d) < n:
        i = np.random.normal(0, n*2, 1)
        d[i] = i
    return d


def lookup(d, n):
    t_list = []

    for k in range(13):
        t = 0
        for i in range(1000):
            index = random.randint(0, n*2-1)
            lookup_s = time()
            d.get(index, None)
            lookup_e = time()
            t += lookup_e - lookup_s
        t_list.append(t)

    return np.mean(t_list[1:-2]), np.std(t_list[1:-2])


def insert(d, n):
    t_list = []

    insertlist = range(0, n*2)
    # insertlist = [random.randint(0, i+100000) for i in range(1000)]
    for k in range(13):
        t = 0
        for i in range(1000):
            index = random.choice(insertlist)
            # index = insertlist[k]
            insert_s = time()
            d[index] = index
            insert_e = time()
            t += insert_e - insert_s
        t_list.append(t)

    return np.mean(t_list[1:-2]), np.std(t_list[1:-2])


def runSimpleDict(k):
    x = [i for i in range(10**(k-1), 10**k, 5*10**(k-2))]

    lookup_means = []
    lookup_errs = []
    insert_means = []
    insert_errs = []

    for n in x:
        d = simpleDict(n)
        lookup_mean, lookup_err = lookup(d, n)
        lookup_means.append(lookup_mean)
        lookup_errs.append(lookup_err)
        insert_mean, insert_err = insert(d, n, False)
        insert_means.append(insert_mean)
        insert_errs.append(insert_err)

    outputToCSV(f"lookup1e{k}", x, lookup_means, lookup_errs)
    outputToCSV(f"insert1e{k}", x, insert_means, insert_errs)


def run(fpath=""):
    if fpath:
        lookup_means = []
        lookup_errs = []
        insert_means = []
        insert_errs = []
        dataset = readDataset(fpath)
        d = dictFromDataset(dataset)
        execute(d, n, "lookup")
    else:
        for k in range(4, 8):
            runSimpleDict(k)


if __name__ == "__main__":
    run(sys.argv[1])
