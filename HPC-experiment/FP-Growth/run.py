'''FP-Growth'''
import header as myHeader
import tree as myTree
from time import time
import sys

#----------scan the db-----------
def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
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


def main(db, f_perf=None):
	start = time()
	dbItems = getDBItems(db)
	#end = time()
	#print("get db items:", end - start)
	#start = time()
	fpTree = buildFPTree(db, dbItems)
	#end = time()
	#print("build FP-Tree:", end - start)
	#start = time()
	results = mineAll(fpTree, '')
	end = time()
	f_perf.write(str(end - start) + "\n\n")
	return sorted(results)

if __name__ == '__main__':
	args = sys.argv
	db = scanDB(args[2], ' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	for num in range(int(args[1])):
		num += 1
		numStr = f'{num:02}'
		f_perf = open(args[3] + numStr + ".txt", 'a')
		f_result = open(args[4] + numStr + ".txt", 'a')
		for i in range(0, 50, 5):
			minsup = i / 100 * len(db)
			f_perf.write(str(i) + ",")
			results = main(db, f_perf)
			f_result.write(str(i) + "\n")
			f_result.write(str(results) + "\n\n")
		f_perf.close()
		f_result.close()
