
""" the issue of `global shared state` """

class SharedDataDescriptor:
    def __init__(self, initial_value):
        self. value = initial_value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        self.value = value


class ClientClass:
    descriptor = SharedDataDescriptor("first value")

# In this example, the descriptor object stores the data itself;
# This carries with it the inconvenience that when we modify the value
# for an instance all other instances of the same classes are also modified
# with this value as well

client1 = ClientClass()
print(client1.descriptor)

client2 = ClientClass()
print(client2.descriptor)

client2.descriptor = "value for client 2"
print(client2.descriptor)

print(client1.descriptor)



""" using weak references """

from weakref import WeakKeyDictionary

class DescriptorClass:
    def __init__(self, initial_value):
        self.value = initial_value
        self.mapping = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.mapping.get(instance, self.value)

    def __set__(self, instance, value):
        self.mapping[instance] = value
