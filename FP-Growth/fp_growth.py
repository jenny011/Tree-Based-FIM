'''FP-Growth'''
import header as myHeader
import tree as myTree

#-------define global vars------
minsup = 1500

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
def buildFPTree(db):
	fpTree = myTree.FPTree()
	dbItems = getDBItems(db)
	# print("db items:", dbItems)
	fpTree.createHeaderTable(dbItems, minsup)
	# print("header table count sum:", sum(fpTree.headerTable.counts()))
	# print("header table:", fpTree.headerTable)
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
	# print("header table:", condTree.headerTable)
	for ptn in condPB:
		condTree.add(ptn[1], ptn[0])
	return condTree

#-----------mine an fp-tree for a pattern-----------
def mine(tree, header, basePtn):
	basePtn += header._key + ' '
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
		# print(condTree)
		patterns += mineAll(condTree, basePtn)
	return patterns

#-----------mine an fp-tree-----------
def mineAll(tree, basePtn):
	allPatterns = []
	for header in tree.headerTable.headers():
		allPatterns += mine(tree, header, basePtn)
	return allPatterns


def main():
	db = scanDB('../datasets/chess.dat', ' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	fpTree = buildFPTree(db)
	print(mineAll(fpTree, ''))
	# print("fpTree size:", fpTree.size())
	# print("fpTree count sums:", sum(fpTree.counts()))
	# print(fpTree)
	# print('LL: ', fpTree.repr_ll('29'))

if __name__ == '__main__':
	main()

