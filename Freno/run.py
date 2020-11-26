'''FRENO'''
from tree import *
from time import time
import sys

def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
	f.close()
	return db


if __name__ == '__main__':
	args = sys.argv
	# db = scanDB(args[2], ' ')
	db = scanDB("../retail.txt", ' ')
	# db = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd', 'e'], ['b', 'c', 'e'], ['b', 'c', 'd', 'e']]
	for num in range(int(args[1])):
		num += 1
		numStr = f'{num:02}'
		#f_perf = open(args[3] + numStr + ".txt", 'a')
		#f_result = open(args[4] + numStr + ".txt", 'a')
		for i in range(1, 2):
			minsup = i / 100 * len(db)
			print(minsup)
			#f_perf.write("\n" + str(i) + ",")
			start = time()
			FrenoTree = Tree(minsup)
			for trx in db:
				trx.sort()
				FrenoTree.insert(FrenoTree._root, trx)
			end = time()
			print(FrenoTree)
			#f_perf.write(str(end - start) + "\n")
			#f_result.write("\n" + str(i) + "\n")
			#f_result.write(str(FrenoTree) + "\n")
		#f_perf.close()
		#f_result.close()
