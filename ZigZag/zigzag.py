import sys, os, argparse
import json, csv
from time import time
from utils import *

def isSubSequence(itemset, trx):
    i = 0
    for j in range(len(trx)):
        if itemset[i] == trx[j]:
            i += 1
        if i >= len(itemset):
            return j
    return False

def isSubSet(itemset, mfi):
    for item in itemset:
        if item not in mfi:
            return False
    return True

def countItemset(itemset):
    sup = 0
    for trx in db:
        if isSubSequence(itemset, trx):
            sup += 1
    return sup


# fiBackTrace([], dbItems, 0, minsup)
# the extension after each c constructs the possible set of the c
def fiBackTrack(itemset, combineSet, index, res):
    for c in combineSet:
        newItemset = itemset + [c]
        res.append(newItemset)
        newPossibleSet = [x for x in combineSet if x > c]
        newCombineSet = fiCombine(newItemset, newPossibleSet)
        fiBackTrack(newItemset, newCombineSet, index + 1, res)
    return res

# the frequent itemset extensions constructs the new combine set
def fiCombine(itemset, possibleSet):
    combineSet = []
    for p in possibleSet:
        temp = itemset + [p]
        if countItemset(temp) >= minsup:
            combineSet.append(p)
    return combineSet

# mfiBackTrace([], dbItems, 0, minsup)
def mfiBackTrack(itemset, combineSet, index):
    for c in combineSet:
        newItemset = itemset + [c]
        newPossibleSet = [x for x in combineSet if x > c]
        for i in mfi:
            if isSubSet(newItemset + newPossibleSet, i):
                return
        newCombineSet = fiCombine(newItemset, newPossibleSet)
        if not newCombineSet:
            for j in mfi:
                if isSubSet(newItemset, j):
                    break
            mfi.add(newItemset)
        else:
            mfiBackTrack(newItemset, newCombineSet, index + 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argparse')
    # parser.add_argument('--expnum', '-n', help='experiment number', required=True)
    parser.add_argument('--dbdir', '-b', help='database directory', required=True)
    parser.add_argument('--db', '-d', help='database name', required=True)
    parser.add_argument('--minsup', '-m', help='minimum support X%', required=True)
    # parser.add_argument('--perf', '-p', help='performance output', required=True)
    # parser.add_argument('--result', '-r', help='result output', required=True)
    args = parser.parse_args()

    db = get_DB(args.dbdir, args.db)
    db_size = len(db)
    dbItems = getDBItems(db)

    minsup = int(args.minsup) / 100 * db_size

    vdb = transposeDB(db)
    f = [k for k, v in dbItems.items() if v >= minsup]

    mfis = {}
    res = fiBackTrack([], f, 0, [])
    print(">>>", res)
