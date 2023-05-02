
# `non-data descriptor` because it doesn't implement the `__set__` magic method

class NonDataDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return 42

class ClientClass:
    descriptor = NonDataDescriptor()


client = ClientClass()
print(client.descriptor)
# if we change the attribute -> we lose access to this value
client.descriptor = '43'
print(client.descriptor)
# but if we delete the descriptor
del client.descriptor
print(client.descriptor)

# when we create the `client` object, the `descriptor` attribute lay in the class,
# not the instance, so if we ask for the dictionary of the `client` object, it
# will be empty
print(vars(client))
# when we request the `.descriptor` attribute, it doesn't find any key in
# `client.__dict__` named "descriptor", so it goes to the class,
# where it will find it ... but only as a descriptor,
# hence why it returns the result of the `__get__` method;
client.descriptor = 99
# sets this value into the dictionary of the instance
print(vars(client))
