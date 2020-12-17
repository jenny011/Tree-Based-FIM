'''FRENO'''
from tree import *
from time import time

def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
	f.close()
	return db


if __name__ == '__main__':
	# db = scanDB('../datasets/retail.txt',' ')
	db = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'b', 'c'], ['a', 'd']]
	for i in range(24, 25):
		minsup = i / 100 * len(db)
		FrenoTree = Tree(minsup)
		start = time()
		for trx in db:
			trx.sort()
			FrenoTree.insert(FrenoTree._root, trx)
		end = time()
		print("\nbuild tree:", end - start)
		print(str(FrenoTree))