# from time import time
from Freno import minsup

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
        self._comb_table = {}
        self._item_table = {}

    def addChild(self, node):
        self._children[node._key] = node


class Tree():
    def __init__(self):
        self._root = TreeNode()
        self._size = 0

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
        ret = ''
        for item in self: 
            if item._count >= minsup:                     
                ret += '{' + item._key + '}, '
        return ret 

    def _addNode(self, parent, value, count=0):
        newNode = TreeNode(value, parent, count)
        parent.addChild(newNode)
        self._size += 1
        return newNode

    def _incrementCount(self, node, count=1):
        node._count += count

    def _recordInfo(self, node, comb, count=1):
        # record combination
        combStr = (",").join(comb)
        node._comb_table[combStr] = node._comb_table.get(combStr, 0) + count
        # record item
        for item in comb:
            node._item_table[item] = node._item_table.get(item, 0) + count
        for item in comb:
            # item just became frequent
            if node._item_table[item] >= minsup and (node._key + "," + item) not in node._children:
                # add node (suitor)
                newNode = self._addNode(node, node._key + "," + item, node._item_table[item])
                # transfer patterns to newNode
                for key in list(node._comb_table.keys()):
                    recorded_ptns = key.split(",")
                    if item in recorded_ptns:
                        i = recorded_ptns.index(item)
                        if i < len(key):
                            suffix = recorded_ptns[recorded_ptns.index(item) + 1:]
                            self._recordInfo(newNode, suffix, node._comb_table[key])
                    # move the whole combination to the child
                    if node._comb_table[key] >= minsup:
                        del node._comb_table[key]

    # insert a combination recursively
    def insertAndRecord(self, node, comb):
        # not root
        # print("+", node._key, node._count,node._item_table)
        self._incrementCount(node)
        # reached the end
        if not comb:
            return
        # matches a child
        if node._key + "," + comb[0] in node._children.keys():
            self.insertAndRecord(node._children[node._key + "," + comb[0]], comb[1:])
        # no match, record the trx at the current node
        else:
            self._recordInfo(node, comb)
        # print("=",node._key, node._count,node._item_table)

    # insert a transaction (from root)
    def insert(self, node, trx):
        for i in range(len(trx)):
            if trx[i] not in node._children.keys():
                newNode = self._addNode(node, trx[i])
            self.insertAndRecord(node._children[trx[i]], trx[i+1:])

    






