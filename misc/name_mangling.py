
""" Name Mangling in Python """
# the purpose is to prevent accidental reusing of variables
# name mangling happens at compile time


class A:
    # becomes _A__count
    # mangled version of the variable
    # <_ClassName__var_name>
    __count = 0
    count = 0 # will work for a.count = 42
    # but
    # self.__len__ = ... double underscores on both sides
    # self.__ = ...
    # NOT MENGLED
    __y = 0 # -> _A__y local
    import __abc # imports _A__abc
    # unless import has a . in its name
    import __abc.a # imports __abc.a

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count


class Widget:
    __count = 0 # _Widget__count

    def __init__(self):
        super().__init__()
        self.__count = Widget.__count
        Widget.__count += 1

    @property
    def widget_id(self):
        return self.__count

    @staticmethod
    def total_widgets_created():
        return Widget.__count


class Button(Widget):
    def __init__(self):
        super().__init__()
        self.__count = 0 # _Button__count

    def click(self):
        self.__count += 1

    def total_clicks(self):
        return self.__count



def main_problem():
    a = A()
    print(a.get_count())

    a.__count = 42 # dosn't change variable
    print(a.get_count())
    a.set_count(42) # changes it
    print(a.__count) # still returns 0???

def main():
    a = A()
    a.__count = 42
    a.set_count(100)
    # Private Name Mangling
    print(a.__dict__) # {'__count': 42, '_A__count': 100}
    a._A__count = 42


if __name__ == '__main__':
    # main_problem()
    main()
