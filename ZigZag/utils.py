import sys, os, argparse
import json, csv

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
