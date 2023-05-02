
""" the Iterator Pattern in Python """
# an iterable object
#   - one that implements __iter__
# an iterator
#   - implements __next__
#
# Interface for iteration

class SequenceIterator:
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step

    def __next__(self):
        value = self.current
        self.current += self.step
        return value

def main_simple_iterator():
    si = SequenceIterator(1, 2)
    next(si)
    next(si)
    try:
        for _ in SequenceIterator(): pass
    except Exception as e: print("oops")
    # error message, no __iter__() implementation
# if an object implements the __iter__() magic method, it means it
# can be used in a for loop

# Sequence objects as iterables

class MappedRange:
    """Apply a transformation to a range of numbers."""

    def __init__(self, transformation, start, end):
        self._transformation = transformation
        self._wrapped = range(start, end)

    def __getitem__(self, index):
        value = self._wrapped.__getitem__(index)
        result = self._transformation(value)
        print("Index {}: {}".format(index, result))
        return result

    def __len__(self):
        return len(self._wrapped)


def main_simple_sequence():
    mr = MappedRange(abs, -10, 5)
    print(mr[0])
    print(mr[-1])
    print(list(mr))















def main():
    main_simple_iterator()
    main_simple_sequence()


if __name__ == '__main__':
    main()
