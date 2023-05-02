
""" Dependency Inversion """

def simple():
    class LightBulb:
        def turn_on(self):
            print("LightBulb: turned on...")

        def turn_off(self):
            print("LightBulb: turned off...")

    class ElectricPowerSwitch:

        def __init__(self, l: LightBulb):
            self.LightBulb = l
            self.on = False

        def press(self):
            if self.on:
                self.LightBulb.turn_off()
                self.on = False
            else:
                self.LightBulb.turn_on()
                self.on = True

    l = LightBulb()
    switch = ElectricPowerSwitch(l)
    switch.press()
    switch.press()


def dependency_inversion():
    from abc import ABC, abstractmethod

    class Switchable(ABC):
        @abstractmethod
        def turn_on(self):
            pass

        @abstractmethod
        def turn_off(self):
            pass

    class LightBulb(Switchable):
        def turn_on(self):
            print("LightBulb: turned on...")

        def turn_off(self):
            print("LightBulb: turned off...")

    class Fan(Switchable):
        def turn_on(self):
            print("Fan: turned on...")

        def turn_off(self):
            print("Fan: turned off...")

    class ElectricPowerSwitch:

        def __init__(self, l: Switchable):
            self.LightBulb = l
            self.on = False

        def press(self):
            if self.on:
                self.LightBulb.turn_off()
                self.on = False
            else:
                self.LightBulb.turn_on()
                self.on = True

    l = LightBulb()
    f = Fan()
    switch = ElectricPowerSwitch(f)
    switch.press()
    switch.press()


if __name__ == "__main__":
    simple()
    dependency_inversion()
