
# smth to be `iterable` broadly speaking it means it can be looped over, but more
# specifically it means that the object needs to return an iterator object from
# its dunder itter method and the iterator that is returned from dunder itter
# must define a dunder next method which accesses elements in the container one
# at a time; because smth is iterable doesn't mean it is an iterator
''' Iterators & Iterables '''
# list is an iterable, but not an iterator;
# iterable is smth that can be looped over;
# __iter__() dunder method, special method, magic method;
nums = [_ for _ in range(10)]
assert '__iter__' in dir(nums)
# assert '__next__' in dir(nums) # raises AssertionError
# an `iterator` is an object with a state so that it remembers where it is during iteration;
i_nums = nums.__iter__() # create an iterator, the same as iter(nums)
assert '__next__' in dir(i_nums)
try: # looping iterator
    while True:
        print(next(i_nums), end=' ')
except StopIteration as e: # raises StopIteration exception
    print(e)
finally:
    print(i_nums) # <list_iterator object at 0x0000000000000000>

class MyRange:

    def __init__(self, start, end):
        self.value = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.value >= self.end:
            raise StopIteration
        current = self.value
        self.value += 1
        return current

nums = MyRange(0, 10)
print(nums)
for num in nums:
    print(num, end=' ')
# print(next(nums)) # raises StopIteration exception !!!
print()
# generators are easy-to-read iterators, functions that yield a value;
# dunder methods created automatically;
def my_range(start, end):
    current = start
    while current < end:
        yield current
        current += 1

nums = my_range(0, 10)
print(nums)
for num in nums:
    print(num, end=' ')
# print(next(nums)) # ALSO raises StopIteration exception !!!

def main():
    print('example:')

    class Sentence:

        def __init__(self, sentence):
            self.sentence = sentence
            self.index = 0
            self.words = self.sentence.split()

        def __iter__(self):
            return self

        def __next__(self):
            if self.index >= len(self.words):
                raise StopIteration
            index = self.index
            self.index += 1
            return self.words[index]

    my_sentence = Sentence('This is a test')

    for word in my_sentence:
        print(word)

    # generator function
    def sentence(sentence):
        for word in sentence.split():
            yield word

    my_sentence = sentence('Another test with generator')
    print(next(my_sentence))
    print(next(my_sentence))

if __name__ == '__main__':
    main()
