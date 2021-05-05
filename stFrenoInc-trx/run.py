'''FRENO'''
from time import time
import sys
import csv, json
import numpy as np

def scanDB(path, separator):
	db = []
	f = open(path, 'r')
	for line in f:
		if line:
			db.append(line.rstrip().split(separator))
	f.close()
	return db

def output_perf(fpath, minsup, perf):
	with open(fpath, 'a') as fperf:
		writer = csv.writer(fperf)
		#writer.writerow([minsup, perf])
		for item in perf:
			writer.writerow(item)

def isSubSequence(l1, l2):
    i = 0
    for j in range(len(l2)):
        if l1[i] == l2[j]:
            i += 1
        if i >= len(l1):
            return j
    return False

class TreeNode():
    def __init__(self, key = None, parent = None, count = 0):
        self._key = key
        self._parent = parent
        self._count = count
        self._children = {}
        self._item_table = {}

    def addChild(self, node):
        self._children[node._key] = node


class Tree():
	def __init__(self, minsup, database={}):
		self._database = database
		self._root = TreeNode()
		self._size = 0
		self.minsup = minsup
		self._times = []

    #-------------------------- public accessors -------------------
	def size(self):
		return self._size

	def is_empty(self):
		return self.size() == 0

	#iterators
	def __iter__(self):
		for node in self.preorder():
			yield node

	def nodes(self):
		for node in self.preorder():
			yield node

	def keys(self):
		for node in self.preorder():
			yield node._key

	def counts(self):
		for node in self.preorder():
			yield node._count

	def children(self, node):
		for child in node._children.keys():
			yield child

	def preorder(self):
		if not self.is_empty():
			for node in self._subtree_preorder(self._root):
				yield node

	def _subtree_preorder(self, node):
		yield node
		for c in node._children.values():
			for other in self._subtree_preorder(c):
				yield other

	def __repr__(self):
		ret = []
		for item in self:
			if item._count >= self.minsup:
				ret.append(str(item._key))
		return str(sorted(ret))

	def toList(self):
		ret = []
		for item in self:
			if item._count >= self.minsup:
				ret.append(str(item._key))
		return sorted(ret)

	def _addNode(self, parent, value, count=0):
		newNode = TreeNode(value, parent, count)
		parent.addChild(newNode)
		self._size += 1
		return newNode

	def _recordAccess(self, node):
		node._count += 1

	def _recordInfo(self, node, comb, index, count=1):
		combStr = (",").join(comb)
		for item in comb:
			node._item_table[item] = node._item_table.get(item, 0) + count
		for item in comb:
			# item just became frequent
			if node._item_table[item] >= self.minsup and (node._key + "," + item) not in node._children:
				# add node
				newNode = self._addNode(node, node._key + "," + item, node._item_table[item])
				# transfer patterns to newNode
				for ptn in db[:index+1]:
					i = isSubSequence(node._key.split(",") + [item], ptn)
					if i:
						if i < len(ptn) - 1:
							suffix = ptn[i + 1:]
							self._recordInfo(newNode, suffix, index)


	def insertAndRecord(self, node, comb, index):
		# not root
		self._recordAccess(node)
		# reached the end
		if not comb:
			return
		self._recordInfo(node, comb, index)
		for i in range(len(comb)):
			if node._key + "," + comb[i] in node._children:
				self.insertAndRecord(node._children[node._key + "," + comb[i]], comb[i+1:], index)

	def insert(self, node, trx, index):
		for i in range(len(trx)):
			if trx[i] not in node._children:
				newNode = self._addNode(node, trx[i])
			self.insertAndRecord(node._children[trx[i]], trx[i+1:], index)



if __name__ == '__main__':
	args = sys.argv
	db = scanDB(args[2], ' ')
	for num in range(int(args[1])):
		num += 1
		numStr = f'{num:02}'
		f_perf = open(args[3] + numStr + ".txt", 'a')
		result = {}
		for i in range(1, 51, 5):
			minsup = i / 100 * len(db)
			# print(minsup, len(db))
			f_perf.write(str(i) + ",")
			FrenoTree = Tree(minsup)
			for j in range(50000):
				trx = db[j]
				trx.sort()
				FrenoTree.insert(FrenoTree._root, trx, j)

			# incremental
			times = []
			for j in range(50000, 51000):
				start = time()
				trx = db[j]
				trx.sort()
				FrenoTree.insert(FrenoTree._root, trx, j)
				end = time()
				times.append(end-start)

			mean_time = np.mean(times)
			err_time = np.std(times)
			# print(end-start)
			# print(FrenoTree)
			f_perf.write(str(mean_time) + "," + str(err_time) + "\n\n")

			result[i] = FrenoTree.toList()
		f_perf.close()
		with open(args[4] + numStr + ".json", "w") as f_result:
			json.dump(result, f_result)
