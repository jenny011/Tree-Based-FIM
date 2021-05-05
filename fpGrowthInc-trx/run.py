'''FP-Growth'''
import header as myHeader
import tree as myTree
from time import time
import sys, os
import argparse
import numpy as np

#----------scan the db-----------
def scanDB(path, separation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(separation))
	f.close()
	return db

#-----------get item counts for a dataset---------
def getDBItems(db):
	dbItems = {}
	for trx in db:
		for item in trx:
			dbItems[item] = dbItems.get(item, 0) + 1
	return dbItems

#-----------build an fp-tree-----------
def buildFPTree(db, dbItems):
	fpTree = myTree.FPTree()
	fpTree.createHeaderTable(dbItems, minsup)
	for trx in db:
		fpTree.add(trx, 1)
	return fpTree

#-----------get item counts for a pattern base-----------
def getPBItems(pb):
	pbItems = {}
	for ptn in pb:
		for item in ptn[1]:
			pbItems[item] = pbItems.get(item, 0) + ptn[0]
	return pbItems

#-----------build a conditional fp-tree-----------
def buildCondTree(condPB):
	condTree = myTree.FPTree()
	pbItems = getPBItems(condPB)
	condTree.createHeaderTable(pbItems, minsup)
	for ptn in condPB:
		condTree.add(ptn[1], ptn[0])
	return condTree

#-----------mine an fp-tree for a pattern-----------
def mine(tree, header, basePtn):
	basePtn += header._key + ','
	patterns = [basePtn]
	ptr = header._next
	condPB = []
	while ptr:
		ptn = tree.prefix_path(ptr)
		if ptn:
			condPB.append(ptn)
		ptr = ptr._next
	if len(condPB) > 0:
		condTree = buildCondTree(condPB)
		patterns += mineAll(condTree, basePtn)
	return patterns

#-----------mine an fp-tree-----------
def mineAll(tree, basePtn):
	allPatterns = []
	for header in tree.headerTable.headers():
		allPatterns += mine(tree, header, basePtn)
	return allPatterns
	

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
	return scanDB(os.path.join(DBDIR, DBFILENAME), " ")


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='argparse')
	parser.add_argument('--expnum', '-n', help='experiment number', required=True)
	parser.add_argument('--dbdir', '-b', help='database directory', required=True)
	parser.add_argument('--db', '-d', help='database name', required=True)
	parser.add_argument('--perf', '-p', help='performance output', required=True)
	parser.add_argument('--result', '-r', help='restult output', required=False)
	args = parser.parse_args()

	totalDB = get_DB(args.dbdir, args.db)
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	for num in range(int(args.expnum)):
		num += 1
		numStr = f'{num:02}'
		f_perf = open(args.perf + numStr + ".txt", 'a')
		for i in range(41, 51, 5):
			minsup = i / 100 * len(totalDB)

			db = totalDB[:50000]
			dbItems = getDBItems(db)
			fpTree = buildFPTree(db, dbItems)
			f_perf.write(str(i) + ",")

			# incremental
			times = []
			for j in range(50000, 51000):
				trx = totalDB[j]
				start = time()
				db.append(trx)
				newDBItems = getDBItems(db)
				unsorted = {}
				for key, count in newDBItems.items():
					if count >= minsup:
						unsorted[key] = count
				temp = sorted(unsorted.items(), key=lambda x: x[1], reverse=True)
				temp_keys = [item[0] for item in temp]
				headers = list(fpTree.headerTable.keys())

				if temp_keys == headers:
					fpTree.add(trx, 1)
					results = mineAll(fpTree, '')
				else:
					fpTree = buildFPTree(db, newDBItems)
					results = mineAll(fpTree, '')
				end = time()
				times.append(end - start)

			mean_times = np.mean(times)
			err_times = np.std(times)
			f_perf.write( str(mean_times) + "," + str(err_times) + "\n\n")	
		f_perf.close()

