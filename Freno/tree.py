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
        self._patterns = {}
        self._items = {}

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

    def _insert(self, parent, value, count=0):
        newNode = TreeNode(value, parent, count)
        parent.addChild(newNode)
        self._size += 1
        return newNode

    def insertCombination(self, node, comb):
        # print("+", node._key, node._count,node._items)
        # if root pass down to first level
        if node == self._root:
            if comb[0] not in node._children:
                newNode = self._insert(node, comb[0])
            return self.insertCombination(node._children[comb[0]], comb[1:])
        # if not root record access
        node._count += 1
        # last item in the combination
        if not comb:
            return
        # the next pattern is frequent
        if node._key + "," + comb[0] in node._children:
            return self.insertCombination(node._children[node._key + "," + comb[0]], comb[1:])
        # the next pattern is not frequent
        else:
            # record pattern
            pattern = (",").join(comb)
            node._patterns[pattern] = node._patterns.get(pattern, 0) + 1
            # record item
            for item in comb:
                node._items[item] = node._items.get(item, 0) + 1
                # item becomes frequent
                if node._items[item] >= minsup:
                    # add node
                    self._insert(node, node._key + "," + item, node._items[item])
                    # transfer patters and items

                    
        # print("=",node._key, node._count,node._items)






