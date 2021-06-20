import sys, os, argparse
import json, csv
from time import time
from utils import *


### save all partial or save freq?
### diffset

class GenMax:
    def __init__(self, minsup, db):
        self.minsup = minsup
        self.db = db
        self.mfis = []
        self.vdb = {}
        self.flist = []

    # Optimize
    def get_tlist(self, itemset):
        if ",".join(itemset) not in self.vdb:
            for i in range(1, len(itemset)):
                temp = ",".join(itemset[:i])
                next = ",".join(itemset[:i+1])
                if next not in self.vdb:
                    self.vdb[next] = self.vdb[temp].intersection(self.vdb[itemset[i]])

    def transposeDB(self):
        self.vdb = transposeDB(self.db)

    def getFlist(self):
        freqDBItems = getFreqDBItems(self.db, self.minsup)
        self.flist = ascOrderedList(freqDBItems)

    def isNotSubSetPosition(self, itemset, mfi):
        for i in range(len(itemset)):
            if itemset[i] not in mfi:
                return i + 1
        return -1

    def countItemsetVertical(self, itemset, itemsetStr, p):
        self.get_tlist(itemset)
        new_tlist = self.vdb[itemsetStr].intersection(self.vdb[p])

        newItemsetStr = ",".join(sorted(itemset + [p]))
        self.vdb[newItemsetStr] = new_tlist
        return len(new_tlist)

    def fiCombineOrd(self, itemset, possibleSet):
        sortedItemset = sorted(itemset)
        itemsetStr = ",".join(sortedItemset)

        combineSetDict = {}
        for p in possibleSet:
            count = self.countItemsetVertical(sortedItemset, itemsetStr, p)
            
            if count >= self.minsup:
                combineSetDict[p] = count / (len(self.vdb[itemsetStr]) * len(self.vdb[p]))
        combineSet = ascOrderedList(combineSetDict)
        return combineSet

    def prep(self):
        self.transposeDB()
        self.getFlist()

    def run(self):
        self.backTrack([], self.flist, self.mfis)

    def backTrack(self, itemset, combineSet, mfis):
        for c in combineSet:
            newItemset = itemset + [c]
            newPossibleSet = combineSet[combineSet.index(c)+1 : ]
            next = False
            p = -1
            for i in range(len(mfis)):
                new_p = self.isNotSubSetPosition(newItemset + newPossibleSet, mfis[i])
                if new_p == -1:
                    next = True
                elif new_p > p:
                    p = new_p
            if next:
                return
            new_mfis = []
            newCombineSet = self.fiCombineOrd(newItemset, newPossibleSet)
            if not newCombineSet:
                if len(newItemset) >= p:
                    mfis.append(newItemset)
            else:
                new_mfis = [mfi for mfi in mfis if c in mfi]
                self.backTrack(newItemset, newCombineSet, new_mfis)
            for mfi in new_mfis:
                if mfi not in mfis:
                    mfis.append(mfi)

    def generateFIs(self):
        freqItemsets = set()
        for mfi in self.mfis:
            freqItemsets = freqItemsets.union(mypowerset(mfi))
        freqItemsets.discard('')
        return freqItemsets


class ZigZag(GenMax):
    def __init__(self, minsup, db):
        super().__init__(minsup, db)
        self.inc_split = None
        self.incDB = []
        self.vIncDB = {}
        self.retained = {}

    # Optimize
    def get_tlistInc(self, itemset):
        if ",".join(itemset) not in self.vIncDB:
            if len(itemset) == 1 or itemset[0] not in self.vIncDB:
                self.vIncDB[itemset[0]] = set()
            for i in range(1, len(itemset)):
                temp = ",".join(itemset[:i])
                next = ",".join(itemset[:i+1])
                if next not in self.vIncDB:
                    self.vIncDB[next] = self.vIncDB[temp].intersection(self.vIncDB.get(itemset[i], set()))

    # Optimize
    def support(self, itemsetStr, inc=False):
        itemset = itemsetStr.split(",")
        if inc:
            self.get_tlistInc(itemset)
            return len(self.vIncDB[itemsetStr])
        else:
            self.get_tlist(itemset)
            return len(self.vdb[itemsetStr])

    def updateRetainedFIs(self):
        for fi in self.generateFIs():
            if fi in self.retained:
                self.retained[fi] = self.retained[fi] + self.support(fi, True)
            else:
                self.retained[fi] = self.support(fi)

    def mergeDB(self):
        self.db = self.db + self.incDB
        self.transposeDB()
        self.getFlist()
        # for k, v in self.vIncDB.items():
        #     self.vdb[k] = self.vdb.get(k,set()).union(v)

    def transposeDBInc(self):
        self.vIncDB = transposeDB(self.incDB, self.inc_split)

    def update_incDB(self, incDB, inc_split):
        self.incDB = incDB
        self.inc_split = inc_split
        self.transposeDBInc()
        self.mergeDB()

    def countItemsetVerticalInc(self, itemset, itemsetStr, p, newItemsetStr):
        if p in self.vIncDB:
            self.get_tlistInc(itemset)
            new_tlist = self.vIncDB[itemsetStr].intersection(self.vIncDB[p])

            self.vIncDB[newItemsetStr] = new_tlist
            return len(new_tlist)

        return 0

    def fiCombineOrdInc(self, itemset, possibleSet):
        sortedItemset = sorted(itemset)
        itemsetStr = ",".join(sortedItemset)

        combineSetDict = {}
        for p in possibleSet:
            newItemsetStr =  ",".join(sorted(itemset + [p]))
            if newItemsetStr in self.retained:
                count = self.retained[newItemsetStr] + self.countItemsetVerticalInc(sortedItemset, itemsetStr, p, newItemsetStr)
            else:
                count = self.countItemsetVertical(sortedItemset, itemsetStr, p)

            if count >= self.minsup:
                combineSetDict[p] = count / (self.support(itemsetStr) * len(self.vdb[p]))
        combineSet = ascOrderedList(combineSetDict)
        return combineSet

    def runInc(self):
        self.mfis = []
        self.backTrackInc([], self.flist, self.mfis)

    def backTrackInc(self, itemset, combineSet, mfis):
        for c in combineSet:
            newItemset = itemset + [c]
            newPossibleSet = combineSet[combineSet.index(c)+1 : ]
            next = False
            p = -1
            for mfi in mfis:
                new_p = self.isNotSubSetPosition(newItemset + newPossibleSet, mfi)
                if new_p == -1:
                    next = True
                elif new_p > p:
                    p = new_p
            if next:
                return
            new_mfis = []
            newCombineSet = self.fiCombineOrdInc(newItemset, newPossibleSet)
            if not newCombineSet:
                if len(newItemset) >= p:
                    mfis.append(newItemset)
            else:
                new_mfis = [mfi for mfi in mfis if c in mfi]
                self.backTrackInc(newItemset, newCombineSet, new_mfis)
            for mfi in new_mfis:
                if mfi not in mfis:
                    mfis.append(mfi)
