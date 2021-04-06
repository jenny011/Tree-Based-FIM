'''FRENO'''
from tree2 import *
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
		#writer.writerow([minsup, perf])
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
		for i in range(1, 51, 5):
			minsup = i / 100 * len(db)
			# print(minsup, len(db))
			f_perf.write(str(i) + ",")
			start = time()
			FrenoTree = Tree(minsup)
			for trx in db:
				trx.sort()
				FrenoTree.insert(FrenoTree._root, trx)
			end = time()
			# print(end-start)
			# print(FrenoTree)
			f_perf.write(str(end - start) + "\n\n")
			f_result.write(str(i) + "\n")
			f_result.write(str(FrenoTree) + "\n\n")
		f_perf.close()
		f_result.close()
		# print(FrenoTree.exp_results())
		# output_perf("retail_perf_cache01.csv", i, str(end-start))
		# output_perf("retail_perf_cache.csv", i, FrenoTree._cache_times)
		# output_perf("retail_perf_table.csv", i, FrenoTree._table_times)
