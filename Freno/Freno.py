'''FRENO'''
from tree import *

minsup = 15590

def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
	f.close()
	return db


if __name__ == '__main__':
	db = scanDB('../datasets/retail.dat',' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	FrenoTree = Tree()
	for trx in db:
		trx.sort()
		for i in range(len(trx)):
			FrenoTree.insertCombination(FrenoTree._root, trx[i:])
	print(str(FrenoTree))