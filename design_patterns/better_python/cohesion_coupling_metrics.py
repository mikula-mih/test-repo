
""" Quality Metrics: Cohesion & Coupling """
# how easily code can be changed or extended
# `Cohesion` - is a degree to which elements of a certain class or function
#   belong together;
#   function with strong cohesion has a clear responsibility, only one task;
# `Coupling` - is a measure of how dependent two parts of code are on each other;
#   High coupling is bad, because changing part of the program result in change
#   in multiple places;
import string
import random

class VehicleRegistryBAD:
    # if you change something in this code you'll also have to change
    # Application class
    def generate_vehicle_id(self, length):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id):
        return (f"{id[:2]}-"
                f"{''.join(random.choices(string.digits, k=2))}-"
                f"{''.join(random.choices(string.ascii_uppercase, k=2))}")

class ApplicationBAD:
    # does to many things
    # HIGH COUPLING: directly relying on implementaion of VehicleRegistry class
    def register_vehicle(self, brand: string): # !!! LOW COHESION
        # create a registry instance
        registry = VehicleRegistryBAD()

        # generate a vehicle id of length 12
        vehicle_id = registry.generate_vehicle_id(12)

        # now generate a license plate for the vehicle
        # using the first two characters of the vehicle id
        license_plate = registry.generate_vehicle_license(vehicle_id)

        # compute the catalogue price
        catalogue_price = 0
        if brand == "Tesla Model 3":
            catalogue_price = 60000
        elif brand == "Volkswagen ID3":
            catalogue_price = 35000
        elif brand == "BMW 5":
            catalogue_price = 45000

        # compute the tax percentage (default 5% of the catalogue price,
        # except for elctric cars where it is 2%)
        tax_percentage = 0.05
        if brand == "Tesla Model 3" or brand == "Volkswagen ID3":
            tax_percentage = 0.02

        # compute the payable tax
        payable_tax = tax_percentage * catalogue_price

        # print out the vehicle registration information
        print("Registration complete. Vehicle inforamtion:")
        print(f"Brand: {brand}")
        print(f"Id: {vehicle_id}")
        print(f"License plate: {license_plate}")
        print(f"Payable tax: {payable_tax}")


def High_Coupling_Low_Cohesion():
    print("\n\tHigh Coupling & Low Cohesion:\n")
    app = ApplicationBAD()
    app.register_vehicle("BMW 5")
# https://codedocs.org/what-is/grasp-object-oriented-design
# `GRASP` == General Responsibility Assignment Software Patterns (or Principles)
#   is a set of "nine fundamental principles in object design and
#   responsibility assignment" by Craig Larman 1997;.
#
# `Inforamtion Expert` where is the information that your application uses centered;

class VehicleInfo:
    brand: str
    catalogue_price: int
    electric: bool

    def __init__(self, brand, electric, catalogue_price):
        self.brand = brand
        self.electric = electric
        self.catalogue_price = catalogue_price

    def compute_tax(self):
        tax_percentage = 0.05
        if self.electric:
            tax_percentage = 0.02
        return tax_percentage * self.catalogue_price

    def print(self):
        print(f"Brand: {self.brand}")
        print(f"Payable tax: {self.compute_tax()}")

class Vehicle:
    id: str
    license_plate: str
    info: VehicleInfo

    def __init__(self, id, license_plate, info):
        self.id = id
        self.license_plate = license_plate
        self.info = info

    def print(self):
        print(f"ID: {self.id}")
        print(f"License plate: {self.license_plate}")
        self.info.print()

class VehicleRegistry:

    vehicle_info = {}

    def add_vehicle_info(self, brand, electric, catalogue_price):
        self.vehicle_info[brand] = VehicleInfo(brand, electric, catalogue_price)

    def __init__(self):
        self.add_vehicle_info("Tesla Model 3", True, 60000)
        self.add_vehicle_info("Volkswagen ID3", True, 35000)
        self.add_vehicle_info("BMW 5", False, 45000)
        self.add_vehicle_info("Tesla Model Y", True, 75000)

    def generate_vehicle_id(self, length):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def generate_vehicle_license(self, id):
        return (f"{id[:2]}-"
                f"{''.join(random.choices(string.digits, k=2))}-"
                f"{''.join(random.choices(string.ascii_uppercase, k=2))}")

    def create_vehicle(self, brand):
        vehicle_id = self.generate_vehicle_id(12)
        license_plate = self.generate_vehicle_license(vehicle_id)
        return Vehicle(vehicle_id, license_plate, self.vehicle_info[brand])

class Application:

    def register_vehicle(self, brand: string):
        # create a registry instance
        registry = VehicleRegistry()

        # create a vehicle
        return registry.create_vehicle(brand)


def Low_Coupling_High_Cohesion():
    print("\n\tLow Coupling & High Cohesion:\n")
    app = Application()
    vehicle = app.register_vehicle("Tesla Model 3")
    vehicle.print()


if __name__ == "__main__":
    High_Coupling_Low_Cohesion()
    Low_Coupling_High_Cohesion()
