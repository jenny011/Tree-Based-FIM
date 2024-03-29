'''FRENO'''
from tree import *
from memory_profiler import memory_usage
import sys

def scanDB(path, separation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(separation))
	f.close()
	return db

def main(minsup, db):
	FrenoTree = Tree(minsup)
	for trx in db:
		trx.sort()
		FrenoTree.insert(FrenoTree._root, trx)

if __name__ == '__main__':
	args = sys.argv
	db = scanDB(args[2], ' ')
	# db = [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'd', 'e'], ['b', 'c', 'e'], ['b', 'c', 'd', 'e']]
	for num in range(int(args[1])):
		num += 1
		numStr = f'{num:02}'
		f_mem = open(args[3] + numStr + ".txt", 'a')
		for i in range(0, 50, 5):
			minsup = i / 100 * len(db)
			f_mem.write(str(i) + ",")
			mem_usage = memory_usage((main, (minsup, db, ), ), 1)
			f_mem.write(str(mem_usage) + "\n\n")
		f_perf.close()
