
# If the descriptor implements `__set__()`,
# then it will always take precedence,
# no matter what attributes are present in the dictionary of the object;

class DataDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return 42

    def __set__(self, instance, value):
        print("setting {}.descriptor to {}".format(instance, value))
        # beter practice:
        # receive the name of `descriptor` as a parameter and store it
        # internally in the `init` method, so that this one will just use the
        # internal attribute, or, even better, use the __set_name__ method;
        instance.__dict__["descriptor"] = value
        # setattr(instance, "descriptor", value)
        # !!!
        # do not use `setattr()` or the assignment expression directly on
        # the descriptor inside the __set__ method --> triggers an infinite recursion

# The client class already has a reference to the descriptor.
# If we add a reference from the descriptor to the client object,
# we are creating circular dependencies, and these objects will never be
# garbage-collected. Since they are pointing at each other,
# their reference counts will never drop below the threshold for removal;

class ClientClass:
    descriptor = DataDescriptor()


client = ClientClass()
print(client.descriptor)
client.descriptor = 99
print(client.descriptor) # returns descriptor's value
# but set value still exists in dictionary of the object
print(vars(client))
print(client.__dict__["descriptor"])
# deleting the attribute will not work anymore
# del client.descriptor
# because now `descriptor` takes precedence but __delete__() method wasn't
# implemented
