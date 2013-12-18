from django.utils.datastructures import SortedDict


class OrderedSet(object):
    """
    A set which keeps the ordering of the inserted items.
    Currently backs onto SortedDict.
    """

    def __init__(self, iterable=None):
        self.dict = SortedDict(((x, None) for x in iterable) if iterable else [])

    def add(self, item):
        self.dict[item] = None

    def remove(self, item):
        del self.dict[item]

    def discard(self, item):
        try:
            self.remove(item)
        except KeyError:
            pass

    def __iter__(self):
        return iter(self.dict.keys())

    def __contains__(self, item):
        return item in self.dict

    def __nonzero__(self):
        return bool(self.dict)
