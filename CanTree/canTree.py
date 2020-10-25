'''FP-Growth'''
import tree as myTree
from FP_Growth import fpGrowth

#-------define global vars------
minsup = 3180

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
#-----------mine an CanTree for a pattern-----------
def mine(tree, key, value, basePtn, support):
	patterns = []
	if support >= minsup:
		basePtn += key + ' '
		patterns.append(basePtn)
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
		allPatterns += mine(tree, key, value, basePtn, dbItems[key])
	return allPatterns


def main():
	db = scanDB('../datasets/chess.dat', ' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	dbItems = getDBItems(db)
	print(dbItems)
	canTree = buildCanTree(db, dbItems)
	print(mineAll(canTree, '', dbItems))
	# print("fpTree size:", fpTree.size())
	# print("fpTree count sums:", sum(fpTree.counts()))
	# print(canTree)
	# print('LL: ', canTree.repr_ll('c'))

if __name__ == '__main__':
	main()

