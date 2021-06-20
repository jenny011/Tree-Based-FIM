import sys, os, argparse
import json, csv
from itertools import combinations

def get_DB(DBDIR, dbname):
    if dbname == "retail":
        DBFILENAME = "retail.txt"
    elif dbname == "kosarak":
        DBFILENAME = "kosarak.txt"
    elif dbname == "chainstore":
        DBFILENAME = "chainstoreFIM.txt"
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

def scanDB(fpath, delimiter):
    db = []
    with open(fpath, 'r') as f:
        for line in f:
            if line:
                trx = line.rstrip().split(delimiter)
                db.append(trx)
    return db

def getDBItems(db):
	dbItems = {}
	for trx in db:
		for item in trx:
			dbItems[item] = dbItems.get(item, 0) + 1
	return dbItems

def getFreqDBItems(db, minsup):
    dbItems = getDBItems(db)
    ret = {}
    for k, v in dbItems.items():
        if v >= minsup:
            ret[k] = v
    return ret

def transposeDB(hdb, base=0):
	vdb = {}
	for i in range(len(hdb)):
		for item in hdb[i]:
			if item in vdb:
				vdb[item].add(i + base)
			else:
				vdb[item] = {i + base}
	return vdb

def mypowerset(l):
    if len(l) == 0:
        return {''}
    s = mypowerset(l[1:])
    t = set()
    for item in s:
        if item:
            temp = item.split(",") + [l[0]]
            temp.sort()
            t.add(",".join(temp))
        else:
            t.add(l[0])
    s = s.union(t)
    return s

def ascOrderedList(fmap):
    flist = sorted(fmap, key=fmap.get)
    return flist

def insertInOrder(l, x):
    if l[0] > x:
        return [x] + l

    for i in range(len(l)-1):
        if l[i] < x and l[i+1] > x:
            return l[:i+1] + [x] + l[i+1:]

    return l + [x]

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

def generateFIsave(mfis):
    fi = set()
    for mfi in mfis:
        fi = fi.union(powerset(mfi))
    res = set()
    for item in fi:
        res.add(",".join(sorted(item.split(","))))
    return sorted(list(res))
