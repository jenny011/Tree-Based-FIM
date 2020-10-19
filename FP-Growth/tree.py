'''tree'''
import header as myHeader

class TreeNode():
        def __init__(self, key = None, parent = None, count = 0, link = None):
            self._key = key
            self._parent = parent
            self._count = count
            self._children = {}
            self._next = link

class Tree():
    #-------------------------- binary tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = TreeNode()
        self._size = 0

    #-------------------------- public accessors ---------------------------------
    def size(self):
        """Return the total number of elements in the tree."""
        return self._size

    def is_empty(self):
        """Return True if the tree is empty."""
        return self.size() == 0

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for node in self.preorder():                       
            yield (node._key, node._count) 

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
        """Generate a preorder iteration of nodes in the tree."""
        if not self.is_empty():
            for node in self._subtree_preorder(self._root):  # start recursion
                yield node

    def _subtree_preorder(self, node):
        """Generate a preorder iteration of nodes in subtree rooted at node."""
        yield node                                           # visit node before its subtrees
        for c in node._children.values():                        # for each child c
            for other in self._subtree_preorder(c):         # do preorder of c's subtree
                yield other                                   # yielding each to our caller


#----------------------------------- Below are FPTree codes -------------------------------
#----------------------------------- Below are FPTree codes -------------------------------
#----------------------------------- Below are FPTree codes -------------------------------

class FPTree(Tree):
    def __init__(self):
        super().__init__()
        self.headerTable = myHeader.HeaderTable()

    #-------------------------- nonpublic mutators --------------------------
    def _update(self, node, count):
        node._count += count
        return node._count

    def insert_loop(self, ptr, line, count):
        for item in line:
            if item in self.children(ptr):
                self._update(ptr._children[item], count)
                ptr = ptr._children[item]
            else:
                self._size += 1
                newNode = TreeNode(item, ptr)
                self._update(newNode, count)
                prevHeader = self.find_last(item)
                prevHeader._next = newNode
                ptr._children[item] = newNode
                ptr = newNode

    def insert(self, ptr, line, count):
        if not line:
            return
        item = line[0]
        if item in self.children(ptr):
            self._update(ptr._children[item], count)
            ptr = ptr._children[item]
            self.insert(ptr, line[1:], count)
        else:
            self._size += 1
            newNode = TreeNode(item, ptr)
            self._update(newNode, count)
            prevHeader = self.find_last(item)
            prevHeader._next = newNode
            ptr._children[item] = newNode
            ptr = newNode
            self.insert(ptr, line[1:], count)

    #-------------------------- public methods --------------------------
    def createHeaderTable(self,dbItems, minsup):
        unsorted = {}
        for key, count in dbItems.items():
            if count >= minsup:
                unsorted[key] = count
        temp = sorted(unsorted.items(), key=lambda x: x[1], reverse=True)
        for item in temp:
            self.headerTable.insert(item[0], item[1])

    def find_last(self, key):
        ptr = self.headerTable.find_first(key)
        while ptr._next:
            ptr = ptr._next
        return ptr

    def add(self, line, count):
        sortedLine = []
        for key in self.headerTable.keys():
            if key in line:
                sortedLine.append(key)
        self.insert(self._root, sortedLine, count)  

    def __repr__(self):
        r = ''
        for i in self:
            r += str(i) + ' '
        return r

    def iter_ll(self, key):
        ptr = self.headerTable.find_first(key)
        while ptr:
            yield ptr
            ptr = ptr._next

    def repr_ll(self, key):
        r = ''
        for node in self.iter_ll(key):
            r += '(' + node._key + ',' + str(node._count) + ') '
        # r = 0
        # for node in self.iter_ll(key):
        #     r += node._count
        return r

    def prefix_path(self, node):
        path = []
        count = node._count
        node = node._parent
        while node and node != self._root:
            path.append(node._key)
            node = node._parent
        if not path:
            return None
        path.reverse()
        return (count, path)


# def main():
#     t = FPTree()
#     t.insert(['a','b','c'])
#     t.insert(['a','b','d'])
#     t.insert(['a','b','c','d'])
#     t.insert(['b','c','d'])

# main()



