import sys, os, argparse
import json, csv
from time import time
from utils import *


def isNotSubSetPosition(itemset, mfi):
    p = -1
    for i in range(len(itemset)):
        if itemset[i] not in mfi:
            if i > p:
                p = i
    return p

def ascOrderedList(fmap):
    flist = sorted(fmap, key=fmap.get)
    return flist

def countItemset(itemset, p):
    newItemset = itemset + [p]
    sup = 0
    for trx in db:
        if isSubSet(newItemset, trx):
            sup += 1
    return sup

def countItemsetVertical(itemset, p):
    new_tlist = vdb[",".join(itemset)].intersection(vdb[p])
    vdb[",".join(itemset + [p])] = new_tlist
    return len(new_tlist)


# the frequent itemset extensions constructs the new combine set
def fiCombine(itemset, possibleSet):
    combineSet = []
    for p in possibleSet:
        if countItemset(itemset, p) >= minsup:
            combineSet.append(p)
    return combineSet

# the extension after each c constructs the possible set of the c
def fiBackTrack(itemset, combineSet):
    for c in combineSet:
        newItemset = itemset + [c]
        res.append(",".join(newItemset))
        newPossibleSet = combineSet[combineSet.index(c)+1 : ]
        newCombineSet = fiCombine(newItemset, newPossibleSet)
        fiBackTrack(newItemset, newCombineSet)


def fiCombineOrdered(itemset, possibleSet):
    combineSetDict = {}
    for p in possibleSet:
        count = countItemsetVertical(itemset, p)
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
        p = -1
        for i in range(len(mfis)):
            new_p = isNotSubSetPosition(newItemset + newPossibleSet, mfis[i])
            if new_p == -1:
                next = True
            elif new_p > p:
                p = new_p
        if next:
            continue
        newCombineSet = fiCombineOrdered(newItemset, newPossibleSet)
        if not newCombineSet:
            if len(newItemset) >= p:
                mfis.append(newItemset)
        else:
            mfiBackTrack(newItemset, newCombineSet)


def lmfiBackTrack(itemset, combineSet, lmfi):
    for c in combineSet:
        newItemset = itemset + [c]
        newPossibleSet = combineSet[combineSet.index(c)+1 : ]
        next = False
        p = -1
        for i in range(len(lmfi)):
            new_p = isNotSubSetPosition(newItemset + newPossibleSet, lmfi[i])
            if new_p == -1:
                next = True
            elif new_p > p:
                p = new_p
        if next:
            continue
        new_lmfi = []
        newCombineSet = fiCombineOrdered(newItemset, newPossibleSet)
        if not newCombineSet:
            if len(newItemset) >= p:
                lmfi.append(newItemset)
        else:
            new_lmfi = [mfi for mfi in lmfi if c in mfi]
            lmfiBackTrack(newItemset, newCombineSet, new_lmfi)
        for mfi in new_lmfi:
            if mfi not in lmfi:
                lmfi.append(mfi)


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

    vdb = transposeDB(db)

    #----------GenMax----------
    # FI-backtrack
    # res = []
    # fiBackTrack([], freqDBItemList)
    # print("FI>", res)

    # MFI-backtrack
    # mfis = []
    # mfiBackTrack([], f, vdb)
    # print("MFI>", mfis)

    # LMFI-backtrack
    lmfi = []
    lmfiBackTrack([], f, lmfi)
    print("LMFI>", lmfi)
