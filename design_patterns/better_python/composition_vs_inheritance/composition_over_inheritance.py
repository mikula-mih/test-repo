
""" Composition is better than Inheritance """
# if you want to separate responsibilities, create code with higher cohesion
# there's a couple of ways to do it: `inheritance`, `composition`;
# `inheritance` - instead of putting everything in one single big class, create
#   a class hierarchy of classes and subclasses;
# `composotion` - using separate classes to represent separate things in the
#   application and then each of these classes use each other in some meaningful
#   way;
# basically the difference between the: "is" a relationship which is inheritance
# and "has" a relationship which is composition;

from dataclasses import dataclass

@dataclass
class HourlyEmployee:
    """Employee that's paid based on number of worked hours."""

    name: str   # too many responsibilities
    id: int
    commission: float = 100
    contracts_landed: float = 0
    pay_rate: float = 0
    hours_worked: int = 0
    employer_cost: float = 1000

    def compute_pay(self) -> float:
        """Composition how much the employee should be paid."""
        return (
            self.pay_rate * self.hours_worked
            + self.employer_cost
            + self.commission * self.contracts_landed
        )

@dataclass
class SalariedEmployee:
    """Employee that's paid based on a fixed monthly salary."""

    name: str
    id: int
    commission: float = 100
    contracts_landed: float = 0
    monthly_salary: float = 0
    percentage: float = 1

    def compute_pay(self) -> float:
        """Compute how much the employee should be paid."""
        return (
            self.monthly_salary * self.percentage
            + self.commission * self.contracts_landed
        )

@dataclass
class Freelancer:
    """Freelancer that's paid based on number of worked hours."""

    name: str
    id: int
    commission: float = 100
    contracts_landed: float = 0
    pay_rate: float = 0
    hours_worked: int = 0
    vat_number: str = ""

    def compute_pay(self) -> float:
        """Compute how much the employee should be paid."""
        return (
            self.pay_rate * self.hours_worked + self.commission * self.contracts_landed
        )

def main() -> None:
    """Main function."""

    henry = HourlyEmployee(name="Henry", id=123456, pay_rate=50, hours_worked=100)
    print(
        f"{henry.name} worked for {henry.hours_worked} hours and earned ${henry.compute_pay()}."
    )

    sarah = SalariedEmployee(
        name="Sarah", id=47832, monthly_salary=5000, contracts_landed=10
    )
    print(
        f"{sarah.name} landed {sarah.contracts_landed} contracts and earned ${sarah.compute_pay()}."
    )


if __name__ == "__main__":
    main()
