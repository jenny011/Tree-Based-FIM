'''FRENO'''
from tree import *
from time import time
import sys
import csv

def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
	f.close()
	return db

def output_perf(fpath, minsup, perf):
	with open(fpath, 'a') as fperf:
		writer = csv.writer(fperf)
		for item in perf:
			writer.writerow(item)


if __name__ == '__main__':
	args = sys.argv
	db = scanDB(args[2], ' ')
	for num in range(int(args[1])):
		num += 1
		numStr = f'{num:02}'
		f_perf = open(args[3] + numStr + ".txt", 'a')
		f_result = open(args[4] + numStr + ".txt", 'a')
		for i in range(0, 50, 5):
			minsup = i / 100 * len(db)
			f_perf.write(str(i) + ",")
			start = time()
			FrenoTree = Tree(minsup)
			for trx in db:
				trx.sort()
				FrenoTree.insert(FrenoTree._root, trx)
			end = time()
			f_perf.write(str(end - start) + "\n\n")
			f_result.write(str(i) + "\n")
			f_result.write(str(FrenoTree.exp_results()) + "\n\n")
		f_perf.close()
		f_result.close()
