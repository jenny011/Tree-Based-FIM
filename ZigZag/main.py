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

def countItemsetVertical(itemset, p):
    new_tlist = vdb[",".join(itemset)].intersection(vdb[p])
    vdb[",".join(itemset + [p])] = new_tlist
    return len(new_tlist)


def fiCombineOrdered(itemset, possibleSet):
    combineSetDict = {}
    for p in possibleSet:
        count = countItemsetVertical(itemset, p)
        if count >= minsup:
            combineSetDict[p] = count
    combineSet = ascOrderedList(combineSetDict)
    return combineSet


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
    f = ascOrderedList(freqDBItems)

    vdb = transposeDB(db)

    # LMFI-backtrack
    mfis = []
    lmfiBackTrack([], f, mfis)
    print("LMFI>", mfis)
