'''FRENO'''
from tree import *

minsup = 3

def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
	f.close()
	return db


if __name__ == '__main__':
	# db = scanDB('../datasets/retail.dat',' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	db = [['a', 'b', 'c', 'd', 'e'], ['a', 'b', 'c', 'd'], ['a', 'c', 'e'], ['a', 'b', 'c', 'd']]
	FrenoTree = Tree()
	for trx in db:
		trx.sort()
		FrenoTree.insert(FrenoTree._root, trx)
	print(str(FrenoTree))