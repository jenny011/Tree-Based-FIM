import sys, os, argparse
import json, csv
from time import time

def scanDB(path, delimiter):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			trx = line.rstrip().split(delimiter)
			db.append(sorted(trx))
	f.close()
	return db

def verticalDB(path, delimiter):
	vdb = {}
	with open(path, 'r') as f:
		i = 0
		for line in f:
			if line:
				for item in line.rstrip().split(delimiter):
					if item in vdb:
						vdb[item].add(i)
					else:
						vdb[item] = {i}
				i += 1
	return vdb, i

def transposeDB(hdb):
	vdb = {}
	for i in range(len(hdb)):
		for item in hdb[i]:
			if item in vdb:
				vdb[item].add(i)
			else:
				vdb[item] = {i}
	return vdb

def get_DB(DBDIR, dbname):
    if dbname == "retail":
        DBFILENAME = "retail.txt"
    elif dbname == "kosarak":
        DBFILENAME = "kosarak.dat"
    elif dbname == "chainstore":
        DBFILENAME = "chainstore.txt"
    elif dbname == "susy":
        DBFILENAME = "SUSY.txt"
    elif dbname == "record":
        DBFILENAME = "RecordLink.txt"
    elif dbname == "skin":
        DBFILENAME = "Skin.txt"
    elif dbname == "uscensus":
        DBFILENAME = "USCensus.txt"
    elif dbname == "online":
        DBFILENAME = "OnlineRetailZZ.txt"
    return scanDB(os.path.join(DBDIR, DBFILENAME), " ")


def generate_and_filter_candidates(item_list, prev_level=None):
	freq_itemsets = []
	if prev_level:
		for itemset_str in prev_level:
			for item in item_list:
				itemset = itemset_str.split(",")
				if item > itemset[-1]:
					itemset.append(item)
					new_itemset_str = ",".join(itemset)
					if new_itemset_str not in db.keys():
						tid_list = db[itemset_str] & db[item]
						db[new_itemset_str] = tid_list
						if filter_candidate(new_itemset_str, tid_list):
							freq_itemsets.append(new_itemset_str)
	else:
		for item in item_list:
			if filter_candidate(item):
				freq_itemsets.append(item)
	return freq_itemsets

def filter_candidate(itemset, tid_list = None):
	if tid_list:
		return len(tid_list) >= minsup
	else:
		return len(db[itemset]) >= minsup
	


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='argparse')
	parser.add_argument('--expnum', '-n', help='experiment number', required=True)
	parser.add_argument('--dbdir', '-b', help='database directory', required=True)
	parser.add_argument('--db', '-d', help='database name', required=True)
	# parser.add_argument('--minsup', '-m', help='minimum support X%', required=True)
	parser.add_argument('--perf', '-p', help='performance output', required=True)
	parser.add_argument('--result', '-r', help='result output', required=True)
	args = parser.parse_args()

	hdb = get_DB(args.dbdir, args.db)
	db_size = len(hdb)

	for i in range(1, 50, 5):
		minsup = i / 100 * db_size

		start = time()
		db = transposeDB(hdb)
		
		item_list = list(db.keys())
		unique_item_no = len(item_list)
		
		freq_itemsets = []
		prev_level = generate_and_filter_candidates(item_list)
		freq_itemsets.extend(prev_level)
		prev_len = 1
		while prev_level and prev_len <= unique_item_no:
			prev_level = generate_and_filter_candidates(item_list, prev_level)
			freq_itemsets.extend(prev_level)
			prev_len += 1

		end = time()

		with open(args.result, 'w') as f_perf:
			f_perf.write(f'{i}:{end-start}\n')

		with open(args.result, 'w') as f_result:
			json.dump({i: sorted(freq_itemsets)}, f_result)



