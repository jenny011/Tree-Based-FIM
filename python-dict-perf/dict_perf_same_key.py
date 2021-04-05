import os
import sys
import random
from time import time
import numpy as np
import csv
import math

datadir = "/Users/jenny/Desktop/Tree-Based-FIM/datasets"

def outputToCSV(op, x, means, errs):
    with open(os.path.join(os. getcwd(), "results", op + ".csv"), mode = 'w') as f:
        writer = csv.writer(f)
        for i in range(len(means)):
            writer.writerow([x[i], means[i], errs[i]])


#-----from dataset-----
def readDataset(dataset_name):
    dataset = []
    if dataset_name == "kosarak":
        dataset_type = ".dat"
    else:
        dataset_type = ".txt"
    with open(os.path.join(datadir, dataset_name + dataset_type), 'r') as f:
        for line in f:
            dataset.append(line.rstrip())
    return dataset

def dictFromDataset(dataset, size):
    d = {}
    for i in range(size):
        d[dataset[i]] = 0
    return d

def lookupDataset(d, keys):
    t = 0

    for i in range(1000):
        lookup_s = time()
        d.get(keys[i], 0)
        lookup_e = time()
        t += lookup_e - lookup_s

    return t

def insertDataset(d, keys):
    t = 0

    for i in range(1000):
        insert_s = time()
        d[keys[i]] = d.get(keys[i], 0) + 1
        insert_e = time()
        t += insert_e - insert_s

    return t


def runDatasetDict(dataset_name):
    dataset = readDataset(dataset_name)
    lookup_means = []
    lookup_errs = []
    insert_means = []
    insert_errs = []
    sizes = [math.floor(len(dataset)*k/100) for k in range(10, 100, 10)]
    for size in sizes:
        l = dataset[size:]
        keys_lookup = []
        keys_insert = []
        for i in range(1000):
            keys_lookup.append(random.choice(l))
            keys_insert.append(random.choice(l))

        t_lookup = []
        t_insert = []

        for k in range(13):
            d = dictFromDataset(dataset, size)
            t_lookup.append(lookupDataset(d, keys_lookup))
            t_insert.append(insertDataset(d, keys_insert))

        lookup_means.append(np.mean(t_lookup))
        lookup_errs.append(np.std(t_lookup))
        insert_means.append(np.mean(t_insert))
        insert_errs.append(np.std(t_insert))

    outputToCSV("lookup_"+dataset_name, sizes, lookup_means, lookup_errs)
    outputToCSV("insert_"+dataset_name, sizes, insert_means, insert_errs)


#-----uniform-----
def simpleDict(n):
    d = {}
    for i in range(0, n*2, 2):
        d[i] = 0
    return d

def lookup(d, keys):
    t = 0
    for i in range(1000):
        lookup_s = time()
        d.get(keys[i], 0)
        lookup_e = time()
        t += lookup_e - lookup_s
    return t

def insert(d, keys):
    t = 0
    for i in range(1000):
        insert_s = time()
        d[keys[i]] = d.get(keys[i], 0) + 1
        insert_e = time()
        t += insert_e - insert_s
    return t

def runSimpleDict(k):
    x = [i for i in range(10**(k-1), 10**k, 5*10**(k-2))]

    lookup_means = []
    lookup_errs = []
    insert_means = []
    insert_errs = []

    for n in x:
        keysList = range(0, n*2-1)
        keys_lookup = []
        keys_insert = []
        for i in range(1000):
            keys_lookup.append(random.choice(keysList))
            keys_insert.append(random.choice(keysList))

        t_lookup = []
        t_insert = []

        for j in range(13):
            d = simpleDict(n)
            t_lookup.append(lookup(d, keys_lookup))
            t_insert.append(insert(d, keys_insert))

        lookup_means.append(np.mean(t_lookup))
        lookup_errs.append(np.std(t_lookup))
        insert_means.append(np.mean(t_insert))
        insert_errs.append(np.std(t_insert))

    outputToCSV(f"lookup1e{k}", x, lookup_means, lookup_errs)
    outputToCSV(f"insert1e{k}", x, insert_means, insert_errs)


def run(from_dataset):
    if from_dataset:
        datasets = ["retail", "OnlineRetailZZ", "RecordLink", "Skin", "chainstoreFIM", "kosarak", "SUSY"]
        for d in datasets:
            runDatasetDict(d)
    else:
        for k in range(4, 8):
            runSimpleDict(k)


if __name__ == "__main__":
    run(int(sys.argv[1]))
