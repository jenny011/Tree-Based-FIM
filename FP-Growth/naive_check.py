'''FP-Growth'''

#-------define global vars------
minsup = 15590

#----------scan db-----------
def scanDB(path, seperation):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(seperation))
	f.close()
	return db

#-------get db items-----
def getDBItems(db):
	dbItems = {}
	for trx in db:
		for item in trx:
			dbItems[item] = dbItems.get(item, 0) + 1
	return dbItems

def main():
	db = scanDB('../datasets/retail.dat', ' ')
	# db = [['a', 'b', 'c', 'd'],['a', 'c', 'd'],['a', 'c'], ['b', 'd']]
	dbItems = getDBItems(db)
	freq = []
	for k, v in dbItems.items():
		if v >= minsup:
			freq.append(k)
	count = [0 for i in range(2**len(freq)-1)]
	temp = []
	for trx in db:
		for i in range(len(freq)):
			if freq[i] in trx:
				temp.append(freq[i])
		if temp == [freq[0]]:
			count[0] += 1
		elif temp == [freq[1]]:
			count[1] += 1
		elif temp == [freq[2]]:
			count[2] += 1
		elif temp == [freq[0],freq[1]]:
			count[3] += 1
		elif temp == [freq[0],freq[2]]:
			count[4] += 1
		elif temp == [freq[1],freq[2]]:
			count[5] += 1
		elif temp == [freq[0],freq[1],freq[2]]:
			count[6] += 1
		temp = []
		
	# print("fpTree size:", fpTree.size())
	# print("fpTree count sums:", sum(fpTree.counts()))
	# print(fpTree)
	# print('LL: ', fpTree.repr_ll('29'))
	print(count)


if __name__ == '__main__':
	main()

