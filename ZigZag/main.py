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
        if isSubSet(itemset, trx):
            sup += 1
    return sup

def ascOrderedList(fmap):
    flist = sorted(fmap, key=fmap.get)
    return flist


# the extension after each c constructs the possible set of the c
def fiBackTrack(itemset, combineSet):
    for c in combineSet:
        newItemset = itemset + [c]
        res.append(",".join(newItemset))
        newPossibleSet = combineSet[combineSet.index(c)+1 : ]
        newCombineSet = fiCombine(newItemset, newPossibleSet)
        fiBackTrack(newItemset, newCombineSet)

# the frequent itemset extensions constructs the new combine set
def fiCombine(itemset, possibleSet):
    combineSet = []
    for p in possibleSet:
        temp = itemset + [p]
        if countItemset(temp) >= minsup:
            combineSet.append(p)
    return combineSet

def fiCombineOrdered(itemset, possibleSet):
    combineSetDict = {}
    for p in possibleSet:
        temp = itemset + [p]
        count = countItemset(temp)
        if count >= minsup:
            combineSetDict[p] = count
    combineSet = ascOrderedList(combineSetDict)
    return combineSet

# Generate Maximal FIs
def mfiBackTrack(itemset, combineSet):
    for c in combineSet:
        newItemset = itemset + [c]
        newPossibleSet = combineSet[combineSet.index(c)+1 : ]
        next = False
        i = 0
        while i < len(mfis):
            if isSubSet(newItemset + newPossibleSet, mfis[i]):
                next = True
                break
            i += 1
        if next:
            continue
        newCombineSet = fiCombineOrdered(newItemset, newPossibleSet)
        if not newCombineSet:
            while i < len(mfis):
                if isSubSet(newItemset, mfis[i]):
                    break
                i += 1
            mfis.append(newItemset)
        else:
            mfiBackTrack(newItemset, newCombineSet)


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
    minsup = int(args.minsup) / 100 * db_size

    freqDBItems = getFreqDBItems(db, minsup)
    freqDBItemList = list(freqDBItems.keys())
    f = ascOrderedList(freqDBItems)

    # vdb = transposeDB(db)

    #----------GenMax----------
    #FI-backtrack
    # res = []
    # fiBackTrack([], freqDBItemList)
    # print("FI>", res)

    # MFI-backtrack
    mfis = []
    mfiBackTrack([], f)
    print("MFI>", mfis)
