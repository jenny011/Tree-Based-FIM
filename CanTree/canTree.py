'''FP-Growth'''
import tree as myTree
from FP_Growth import fpGrowth
from time import time

#-------define global vars------
minsup = 15590

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

#-----------build an CanTree-----------
def buildCanTree(db, dbItems):
	canTree = myTree.CanTree()
	# print("db items:", dbItems)
	canTree.createRoute(dbItems)
	# print("header table count sum:", sum(fpTree.headerTable.counts()))
	# print("header table:", fpTree.headerTable)
	for trx in db:
		canTree.add(trx, 1)
	return canTree


#-----------mining-----------
#-----------mining-----------
#-----------mining-----------
#-----------mine an CanTree for an item-----------
def mine(tree, key, value, basePtn):
	basePtn += key + ' '
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
		# print(condTree)
		patterns += fpGrowth.mineAll(condTree, basePtn, minsup)
	return patterns

#-----------mine an CanTree-----------
def mineAll(tree, basePtn, dbItems):
	allPatterns = []
	for key, value in tree.route.items():
		if dbItems[key] >= minsup:
			allPatterns += mine(tree, key, value, basePtn)
	return allPatterns


def main():
	db = scanDB('../datasets/retail.dat', ' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	start = time()
	dbItems = getDBItems(db)
	end = time()
	print("get db items:", end - start)
	# print(dbItems)
	start = time()
	canTree = buildCanTree(db, dbItems)
	end = time()
	print("build CANTree:", end - start)
	start = time()
	print(mineAll(canTree, '', dbItems))
	end = time()
	print("mine CANTree:", end - start)
	# print("fpTree size:", fpTree.size())
	# print("fpTree count sums:", sum(fpTree.counts()))
	# print(canTree)
	# print('LL: ', canTree.repr_ll('c'))

if __name__ == '__main__':
	main()

