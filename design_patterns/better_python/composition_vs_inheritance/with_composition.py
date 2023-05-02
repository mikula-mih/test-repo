from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
# with composition we are not creating hierarchies of classes we're trying to
# separate out the concepts and combine them in meaningful way

class Contract(ABC):
    """Represents a contract anda payment process for a particular employeee."""

    @abstractmethod
    def get_payment(self) -> float:
        """Compute how much to pay an employee under this contract."""


@dataclass
class Commission(ABC):
    """Represents a commission payment process."""

    @abstractmethod
    def get_payment(self) -> float:
        """Returns the commission to be paid out."""


@dataclass
class ContractCommission(Commission):
    """Represents a commission payment process based on the number of contracts landed."""

    commission: float = 100
    contracts_landed: int = 0

    def get_payment(self) -> float:
        """Returns the commission to be paid out."""
        return self.commission * self.contracts_landed


@dataclass
class Employee:
    """Basic representation of an employee at the company."""

    name: str
    id: int
    contract: Contract
    commission: Optional[Commission] = None

    def compute_pay(self) -> float:
        """Compute how much the employee should be paid."""
        payout = self.contract.get_payment()
        if self.commission is not None:
            payout += self.commission.get_payment()
        return payout


@dataclass
class HourlyContract(Contract):
    """Contract type for an employee being paid on an hourly basis."""

    pay_rate: float
    hours_worked: int = 0
    employer_cost: float = 1000

    def get_payment(self) -> float:
        return self.pay_rate * self.hours_worked + self.employer_cost


@dataclass
class SalariedContract(Contract):
    """Contract type for an employee being paid a monthly salary."""

    monthly_salary: float
    percentage: float = 1

    def get_payment(self) -> float:
        return self.monthly_salary * self.percentage


@dataclass
class FreelancerContract(Contract):
    """Contract type for a freelancer (paid on an hourly basis)."""

    pay_rate: float
    hours_worked: int = 0
    vat_number: str = ""

    def get_payment(self) -> float:
        return self.pay_rate * self.hours_worked


def main() -> None:
    """Main function."""

    henry_contract = HourlyContract(pay_rate=50, hours_worked=100)
    henry = Employee(name="Henry", id=12346, contract=henry_contract)
    print(
        f"{henry.name} worked for {henry_contract.hours_worked} hours "
        f"and earned ${henry.compute_pay()}."
    )

    sarah_contract = SalariedContract(monthly_salary=5000)
    sarah_commission = ContractCommission(contracts_landed=10)
    sarah = Employee(
        name="Sarah", id=47832, contract=sarah_contract, commission=sarah_commission
    )
    print(
        f"{sarah.name} landed {sarah_commission.contracts_landed} contracts "
        f"and earned ${sarah.compute_pay()}."
    )


if __name__ == "__main__":
    main()

# overall:
# use abstract base classes to define the interfaces and then define
# subclasses for the specific versions of that and patch them up at the end

# in terms of coupling:
# so what you do with an abstract base class is that you're reducing coupling
# between various parts of your application because you're allowing one class
# to depend on the interface instead of a direct instance, that's why
# ABC help you reduce coupling;
# inheritance in general is a mechanism that adds coupling because every time you
# create a subclass that subclass is directly dependent on the superclass so if
# your aim is to reduce coupling in your application;
