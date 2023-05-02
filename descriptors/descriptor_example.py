

class Attribute:
    value = 42

class Client:
    attribute = Attribute()


class DescriptorClass:
    # __get__ required for descriptor
    def __get__(self, instance, owner):
        # instance - refers to the object from which the descriptor is
        # being called --> client
        if instance is None:
            return f"{self.__class__.__name__}.{owner.__name__}"
        print("Call: %s.__get__(%r, %r)",
            self.__class__.__name__, instance, owner)
        return instance


class ClientClass:
    descriptor = DescriptorClass()




def main():
    print(
        Client().attribute, '\n',
        Client().attribute.value
    )
    # descriptor implementation
    client = ClientClass()
    client.descriptor
    print(client.descriptor is client)

if __name__ == '__main__':
    main()
