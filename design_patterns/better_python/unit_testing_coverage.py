
# `Coverage` a measure for how much of your code is tested and is generally
#   expressed as a percentage;
# `test fixtures` give you an environment or context in which your code runs:
#   fake dataset,, mock | stop objects that help you single out a particular
#   piece of code;
# Test-Driven Development
def main_BAD():
    class VehicleInfo:

        def __init__(self, brand, electric, catalogue_price):
            self.brand = brand
            self.electric = electric
            self.catalogue_price = catalogue_price

        # This method computes the tax payable for this particular vehicle and
        # returns that as a positive floating point value.
        # You can optionally provide an amount below which no tax is computed
        def compute_tax(self, tax_exemption_amount: int = 0) -> float:
            if tax_exemption_amount < 0:
                raise ValueError(f"tax_exemption_amount should be a positive number, but received {tax_exemption_amount} instead.")
            tax_percentage = 0.05
            if self.electric:
                tax_percentage = 0.02
            return tax_percentage * (self.catalogue_price - tax_exemption_amount)

        # you can only lease this car if the catalogue price is not more than 70% of
        # your year income; year_income should be >= 0
        def can_lease(self, year_income: int) -> bool:
            # to do
            pass

    # create a vehicle info object
    v = VehicleInfo("BMW", False, 10000)

    # compute the tax
    print(f"BMW tax: {v.compute_tax()}")


class VehicleInfo:

    def __init__(self, brand, electric, catalogue_price):
        self.brand = brand
        self.electric = electric
        self.catalogue_price = catalogue_price

    # This method computes the tax payable for this particular vehicle and
    # returns that as a positive floating point value.
    # You can optionally provide an amount below which no tax is computed
    def compute_tax(self, tax_exemption_amount: int = 0):
        if tax_exemption_amount < 0:
            raise ValueError(f"tax_exemption_amount should be a positive number, but received {tax_exemption_amount} instead.")
        tax_percentage = 0.05
        if self.electric:
            tax_percentage = 0.02
        return tax_percentage * (max(self.catalogue_price - tax_exemption_amount, 0))

    # you can only lease this car if the catalogue price is not more than 70% of
    # your year income; year_income should be >= 0
    def can_lease(self, year_income: int) -> bool:
        if year_income < 0:
            raise ValueError(f"year_income should be a positive number, but received {year_income} instead.")
        return self.catalogue_price <= 0.7 * year_income

import unittest

class TestVehicleInfoMethods(unittest.TestCase):

    def test_compute_tax_non_electric(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertEqual(v.compute_tax(), 500)

    def test_compute_tax_electric(self):
        v = VehicleInfo("BMW", True, 10000)
        self.assertEqual(v.compute_tax(), 200)

    def test_compute_tax_exemption(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertEqual(v.compute_tax(5000), 250)

    def test_compute_tax_exemption_negative(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertRaises(ValueError, v.compute_tax, -5000)

    def test_compute_tax_exemption_high(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertEqual(v.compute_tax(20000), 0)

    def test_can_lease_false(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertEqual(v.can_lease(5000), False)

    def test_can_lease_true(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertEqual(v.can_lease(15000), True)

    def test_can_lease_negative_income(self):
        v = VehicleInfo("BMW", False, 10000)
        self.assertRaises(ValueError, v.can_lease, -5000)

# run the actual unittests
unittest.main()

if __name__ == "__main__":
    main_BAD()
