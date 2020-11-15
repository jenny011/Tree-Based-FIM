'''FRENO'''
from tree import *

minsup = 15000

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
	# db = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd'], ['a', 'c'], ['a', 'b', 'c'], ['a', 'd']]
	FrenoTree = Tree()
	for trx in db:
		trx.sort()
		FrenoTree.insert(FrenoTree._root, trx)
	print(str(FrenoTree))