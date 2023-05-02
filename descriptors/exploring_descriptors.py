
class DescriptorClass:
    def __get__(self, instance, owner):
        if instance is None:
            return f"{self.__class__.__name__}.{owner.__name__}"
        return f"value for {instance}"


class ClientClass:

    descriptor = DescriptorClass()

# creating generic validation objects for attributes, which can be created
# dynamically with functions to validate on the values before assigning them
# to the object
class Validation:

    def __init__(self, validation_function, error_msg: str):
        self.validation_function = validation_function
        self.error_msg = error_msg

    def __call__(self, value):
        if not self.validation_function(value):
            raise ValueError(f"{value!r} {self.error_msg}")

class Field:

    def __init__(self, *validations):
        self._name = None
        self.validations = validations

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def validate(self, value):
        for validation in self.validations:
            validation(value)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._name] = value


class ClientClassV:
    descriptor = Field(
        Validation(lambda x: isinstance(x, (int, float)), "is not a number"),
        Validation(lambda x: x >= 0, "is not >= 0"),
    )


def main():
    print(f"call directly: "
          f"{ClientClass.descriptor}\n"
          f"from created object: "
          f"{ClientClass().descriptor}"
    )
    print("Validation example:")
    client = ClientClassV()
    client.descriptor = 42
    print(client.descriptor)
    # client.descriptor = -42 # invalid value


if __name__ == "__main__":
    main()
