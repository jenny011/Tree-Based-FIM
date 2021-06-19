import sys, os, argparse
import json, csv
from itertools import combinations

def get_DB(DBDIR, dbname):
    if dbname == "retail":
        DBFILENAME = "retail.txt"
    elif dbname == "kosarak":
        DBFILENAME = "kosarak.dat"
    elif dbname == "chainstore":
        DBFILENAME = "chainstore.txt"
    elif dbname == "susy":
        DBFILENAME = "SUSY.txt"
    elif dbname == "record":
        DBFILENAME = "RecordLink.txt"
    elif dbname == "skin":
        DBFILENAME = "Skin.txt"
    elif dbname == "uscensus":
        DBFILENAME = "USCensus.txt"
    elif dbname == "online":
        DBFILENAME = "OnlineRetailZZ.txt"
    elif dbname == "test":
        DBFILENAME = "transData.txt"
    return scanDB(os.path.join(DBDIR, DBFILENAME), " ")

def scanDB(path, delimiter):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			trx = line.rstrip().split(delimiter)
			db.append(sorted(trx))
	f.close()
	return db

def getDBItems(db):
	dbItems = {}
	for trx in db:
		for item in trx:
			dbItems[item] = dbItems.get(item, 0) + 1
	return dbItems

def getFreqDBItems(db, minsup):
    dbItems = {}
    for trx in db:
        for item in trx:
            dbItems[item] = dbItems.get(item, 0) + 1
    ret = {}
    for k, v in dbItems.items():
        if v >= minsup:
            ret[k] = v
    return ret

def verticalDB(path, delimiter):
	vdb = {}
	with open(path, 'r') as f:
		i = 0
		for line in f:
			if line:
				for item in line.rstrip().split(delimiter):
					if item in vdb:
						vdb[item].add(i)
					else:
						vdb[item] = {i}
				i += 1
	return vdb, i

def transposeDB(hdb):
	vdb = {}
	for i in range(len(hdb)):
		for item in hdb[i]:
			if item in vdb:
				vdb[item].add(i)
			else:
				vdb[item] = {i}
	return vdb


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

# def powerset(s):
#     ret = []
#     x = len(s)
#     for i in range(1 << x):
#         l = [s[j] for j in range(x) if (i & (1 << j))]
#         if l:
#             ret.append(",".join(l))
#     return ret

def powerset(l):
    ret = set()
    for i in range(len(l)+1):
        comb = set()
        for element in combinations(l,i):
            temp = ",".join(sorted(element))
            if temp:
                comb.add(temp)
        ret = ret.union(comb)
    return ret
