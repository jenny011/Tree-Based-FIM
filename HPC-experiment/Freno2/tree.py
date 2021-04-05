class Cache():
    def __init__(self, size_limit=800):
        self._cache = {}
        self._min = ()
        self._size = 0
        self._size_limit = size_limit
        self._n = 0

    def __contains__(self, itemset):
        return itemset in self._cache

    def __getitem__(self, itemset):
        return self._cache[itemset]

    def add(self, itemset, count):
        self._cache[itemset] = count
        self._size += 1
        if not self._min or count < self._min[1]:
            self._min = (itemset, count)

    def replace(self, itemset, count):
        ret = self._min
        del self._cache[ret[0]]
        self._cache[itemset] = count
        self._min = (itemset, count)
        return ret

    def delete(self, itemset):
        del self._cache[itemset]
        self._size -= 1

    def update(self, itemset, count):
        self._cache[itemset] += count
        if count < self._min[1]:
            self._min = (itemset, count)

    def full(self):
        return self._size >=  self._size_limit


'''tree'''
#-------------------------- Tree Base -------------------
#-------------------------- Tree Base -------------------
#-------------------------- Tree Base -------------------
class TreeNode():
    def __init__(self, key = None, parent = None, count = 0):
        self._key = key
        self._parent = parent
        self._count = count
        self._children = {}
        self._comb_cache = Cache()
        self._comb_table = {}
        self._item_cache = Cache()
        self._item_table = {}

    def addChild(self, node):
        self._children[node._key] = node


class Tree():
    def __init__(self, minsup):
        self._root = TreeNode()
        self._size = 0
        self.minsup = minsup

    #-------------------------- public accessors -------------------
    def size(self):
        return self._size

    def is_empty(self):
        return self.size() == 0

    #iterators
    def __iter__(self):
        for node in self.preorder():
            yield node

    def __repr__(self):
        ret = []
        for node in self.preorder():
            if node._count >= self.minsup:
                ret.append(node._key)
        return str(ret)

    def exp_results(self):
        ret = []
        s1 = 0
        s2 = 0
        icache = 0
        itable = 0
        ccache = 0
        ctable = 0
        n1 = 0
        n2 = 0
        for node in self.preorder():
            s1 += node._item_cache._n
            icache += node._item_cache._size
            itable += len(node._item_table)
            if node._item_cache.full():
                n1 += 1
            s2 += node._comb_cache._n
            ccache += node._comb_cache._size
            ctable += len(node._comb_table)
            if node._comb_cache.full():
                n2 += 1
        return f'Cache eviction: item - {s1}, comb - {s2}\nItem: cache - {icache}, table - {itable}\nComb: cache - {ccache}, table - {ctable}\nTable used: item - {n1}, comb - {n2}'

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

    def comb_table_size(self):
        s = []
        for item in self:
            s.append(len(item._comb_table))
        return s

    def item_table_size(self):
        s = []
        for item in self:
            s.append(len(item._item_table))
        return s

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

    def _recordInfo(self, node, comb, count=1, exist=True):
        # record pattern
        combStr = (",").join(comb)
        # if comb in cache
        if combStr in node._comb_cache:
            node._comb_cache.update(combStr, count)
        #if comb not in cache
        elif node._comb_cache.full():
            new_count = node._comb_table.get(combStr, 0) + count
            # if count > cache min, replace
            if node._comb_cache._min[1] < new_count:
                ret_comb = node._comb_cache.replace(combStr, new_count)
                # put evicted comb in table
                node._comb_table[ret_comb[0]] = ret_comb[1]
            else:
                node._comb_table[combStr] = new_count
        else:
            node._comb_cache.add(combStr, count)
        # record item
        for item in comb:
            node._item_table[item] = node._item_table.get(item, 0) + count
            # if item in node._item_cache:
            #     node._item_cache.update(item, count)
            # elif node._item_cache.full():
            #     new_count = node._item_table.get(item, 0) + count
            #     if node._item_cache._min[1] < new_count:
            #         ret_item = node._item_cache.replace(item, new_count)
            #         node._item_table[ret_item[0]] = ret_item[1]
            #     else:
            #         node._item_table[item] = new_count
            # else:
            #     node._item_cache.add(item, count)
        # breadth first
        for item in comb:
            # if item in node._item_cache:
            #     if node._item_cache[item] >= self.minsup:
            #         # add node
            #         newNode = self._addNode(node, node._key + "," + item, node._item_cache[item])
            #         # transfer patterns to newNode
            #         for key in node._comb_cache:
            #             ptn = key.split(",")
            #             if item in ptn:
            #                 i = ptn.index(item)
            #                 if i < len(ptn) - 1:
            #                     suffix = ptn[i + 1:]
            #                     self._recordInfo(newNode, suffix, node._comb_cache[key], exist=False)
            #         for key in node._comb_table:
            #             ptn = key.split(",")
            #             if item in ptn:
            #                 i = ptn.index(item)
            #                 if i < len(ptn) - 1:
            #                     suffix = ptn[i + 1:]
            #                     self._recordInfo(newNode, suffix, node._comb_table[key], exist=False)
            # else:
            if node._item_table[item] >= self.minsup:
                # add node
                newNode = self._addNode(node, node._key + "," + item, node._item_table[item])
                # transfer patterns to newNode
                for key in node._comb_cache:
                    ptn = key.split(",")
                    if item in ptn:
                        i = ptn.index(item)
                        if i < len(ptn) - 1:
                            suffix = ptn[i + 1:]
                            self._recordInfo(newNode, suffix, node._comb_cache[key], exist=False)
                for key in node._comb_table:
                    ptn = key.split(",")
                    if item in ptn:
                        i = ptn.index(item)
                        if i < len(ptn) - 1:
                            suffix = ptn[i + 1:]
                            self._recordInfo(newNode, suffix, node._comb_table[key], exist=False)
                    # the whole combination becomes frequent
                    if node._comb_table[key] >= self.minsup:
                        del node._comb_table[key]
                # del node._item_table[item]

    def insertAndRecord(self, node, comb):
        # not root
        self._recordAccess(node)
        # reached the end
        if not comb:
            return
        self._recordInfo(node, comb)
        for i in range(len(comb)):
            if node._key + "," + comb[i] in node._children:
                self.insertAndRecord(node._children[node._key + "," + comb[i]], comb[i+1:])

    def insert(self, node, trx):
        for i in range(len(trx)):
            if trx[i] not in node._children:
                newNode = self._addNode(node, trx[i])
            self.insertAndRecord(node._children[trx[i]], trx[i+1:])
