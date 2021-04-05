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
		#writer.writerow([minsup, perf])
		for item in perf:
			writer.writerow(item)


if __name__ == '__main__':
	# args = sys.argv
	db = scanDB("../datasets/retail.txt", ' ')
	# for num in range(1):
	# 	num += 1
	# 	numStr = f'{num:02}'
	# 	# f_result = open(args[4] + numStr + ".txt", 'a')
	# 	i = 20

	# 	minsup = i / 100 * len(db)
	# 	print(minsup, len(db))
	# 	# f_perf.write(str(i) + ",")
	# 	start = time()
	# 	FrenoTree = Tree(minsup)
	# 	for trx in db:
	# 		trx.sort()
	# 		FrenoTree.insert(FrenoTree._root, trx)
	# 	end = time()
	# 	print(end-start)
	# 	print(FrenoTree)
	# 	print(FrenoTree.exp_results())
		#output_perf("retail_perf_cache01.csv", i, str(end-start))
		# output_perf("retail_perf_cache.csv", i, FrenoTree._cache_times)
		# output_perf("retail_perf_table.csv", i, FrenoTree._table_times)

		# 	f_result.write(str(i) + "\n")
		# 	f_result.write(str(FrenoTree) + "\n\n")
		# f_result.close()
