'''header table'''
class Header():
    __slots__ = '_key', '_count', '_next'

    def __init__(self, key, count, link = None):
      self._key = key
      self._count = count
      self._next = link

    def __gt__(self, other):
      return self._count > other._count 

    def __repr__(self):
      return '({0}: {1})'.format(self._key, self._count)

class HeaderTable(): # maxHeap
    def __init__(self):
        self._table = []

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for header in self._table:  
            yield (header._key, header._count)

    def __repr__(self):
        r = ''
        for i in self:
            r += str(i) + ' '
        return r

    def headers(self):
        for header in self._table:
            yield header

    def keys(self):
        for header in self.headers():  
            yield header._key

    def counts(self):
        for header in self.headers():  
            yield header._count

    def insert(self, key, count):
        self._table.append(Header(key, count))

    def find_first(self, key):
        for header in self.headers():
            if header._key == key:
                return header
