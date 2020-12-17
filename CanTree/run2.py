'''CanTree'''
import tree as myTree
from FP_Growth import fpGrowth
from memory_profiler import memory_usage
import sys


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

#-----------build an CanTree-----------
def buildCanTree(db, dbItems):
	canTree = myTree.CanTree()
	canTree.createHeaderTable(dbItems)
	for trx in db:
		canTree.add(trx, 1)
	return canTree


#-----------mining-----------
#-----------mining-----------
#-----------mining-----------
#-----------mine an CanTree for an item-----------
def mine(tree, key, value, basePtn):
	basePtn += key + ','
	patterns = [basePtn]
	ptr = value
	condPB = []
	while ptr:
		ptn = tree.prefix_path(ptr)
		if ptn:
			condPB.append(ptn)
		ptr = ptr._next
	if len(condPB) > 0:
		condTree = fpGrowth.buildCondTree(condPB, minsup)
		patterns += fpGrowth.mineAll(condTree, basePtn, minsup)
	return patterns

#-----------mine an CanTree-----------
def mineAll(tree, basePtn, dbItems):
	allPatterns = []
	for key, value in tree.headerTable.items():
		if dbItems[key] >= minsup:
			allPatterns += mine(tree, key, value, basePtn)
	return allPatterns


def main(db):
	dbItems = getDBItems(db)
	canTree = buildCanTree(db, dbItems)
	results = mineAll(canTree, '', dbItems)
	return results


if __name__ == '__main__':
	args = sys.argv
	db = scanDB(args[2], ' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	for num in range(int(args[1])):
		num += 1
		numStr = f'{num:02}'
		f_mem = open(args[3] + numStr + ".txt", 'a')
		for i in range(0, 50, 5):
			minsup = i / 100 * len(db)
			f_mem.write(str(i) + ",")
			mem_usage = memory_usage((main, (db,), ), 1)
			f_mem.write(str(mem_usage) + "\n\n")
		f_mem.close()
