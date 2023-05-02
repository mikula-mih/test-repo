"""
Very advanced Employee management system.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List
from enum import Enum, auto

FIXED_VACATION_DAYS_PAYOUT = 5 # The fixed num of vacation days that can be paid out.

class VacationDaysShortageError(Exception):
    """Custom error that is raised when not enough vacation days are available."""

    def __init__(self, requested_days: int, remaining_days: int, message: str) -> None:
        self.requested_days = requested_days
        self.remaining_days = remaining_days
        self.message = message
        super().__init__(message)

class Role(Enum):
    """Employee roles."""

    PRESIDENT = auto()
    VICEPRESIDENT = auto()
    MANAGER = auto()
    LEAD = auto()
    WORKER = auto()
    INTERN = auto()

@dataclass
class Employee(ABC):
    """Basic representation of an employee at the company."""

    name: str
    role: Role
    vacation_days: int = 25

    def take_a_holiday(self, payout: bool) -> None:
        """Let the employee take a single holiday, or pay out 5 holidays."""

        # def take_a_holiday(self, payout: bool) -> None:
        #     """Let the employee take a single holiday, or pay out 5 holidays."""
        #     if payout:
        #         # check that there are enough vacation days left for a payout
        #         if self.vacation_days < FIXED_VACATION_DAYS_PAYOUT:
        #             raise ValueError(
        #                 f"You don't have enough holidays left over for a payout.\
        #                     Remaining holidays: {self.vacation_days}."
        #             )
        #         try:
        #             self.vacation_days -= FIXED_VACATION_DAYS_PAYOUT
        #             print(f"Paying out a holiday. Holidays left: {self.vacation_days}")
        #         except Exception:
        #             # this should never happen
        #             pass
        #     else:
        #         if self.vacation_days < 1:
        #             raise ValueError(
        #                 f"You don't have any holidays left. Now back to work, you!"
        #             )
        #         self.vacation_days -= 1
        #         print("Have fun on your holiday. Don't forget to check your emails!")

    def take_a_holiday(self) -> None:
        """Let the employee take a single holiday."""
        if self.vacation_days < 1:
            raise VacationDaysShortageError(
                requested_days=1,
                remaining_days=self.vacation_days,
                message="You don't have any holidays left. Now back to work, you!",
            )
            # raise ValueError(
            #     f"You don't have any holidays left. Now back to work, you!"
            # )
        self.vacation_days -= 1
        print("Have fun on your holiday. Don't forget to check your emails!")

    def payout_a_holiday(self):
        """Let the employee get paid for unused holidays."""
        # check that there are enough vacation days left for a payout
        if self.vacation_days < FIXED_VACATION_DAYS_PAYOUT:
            raise VacationDaysShortageError(
                requested_days=FIXED_VACATION_DAYS_PAYOUT,
                remaining_days=self.vacation_days,
                message="You don't have enough holidays left over for a payout.",
            )
            # raise ValueError(
            #     f"You don't have enough holidays left over for a payout.\
            #         Remaining holidays: {self.vacation_days}."
            # )

        self.vacation_days -= FIXED_VACATION_DAYS_PAYOUT
        print(f"Paying out a holiday. Holidays left: {self.vacation_days}")

    @abstractmethod
    def pay(self) -> None:
        """Method to call when paying an employee."""


@dataclass
class HourlyEmployee(Employee):
    """Employee that's paid based on number of worked hours."""

    hourly_rate_dollars: float = 50
    hours_worked: int = 10

    def pay(self) -> None:
        print(
            f"Paying employee {self.name} a hourly rate of \
            ${self.hourly_rate} for {self.amount} hours."
        )


@dataclass
class SalariedEmployee(Employee):
    """Employee that's paid based on a fixed monthly salary."""

    monthly_salary: float = 5000

    def pay(self) -> None:
        print(
            f"Paying employee {self.name} a monthly salary of ${self.monthly_salary}."
        )


class Company:
    """Represents a company with employees."""

    def __init__(self) -> None:
        self.employees: List[Employee] = []

    def add_employee(self, employee: Employee) -> None:
        """Add an employee to the list of employees."""
        self.employees.append(employee)

    def find_employee(self, role: Role) -> List[Employee]:
        """Find all employees with a particular role."""
        # Using list comprehensions
        return [employee for employee in self.employees if employee.role is role]
        # employees = []
        # for employee in self.employees:
        #     if employee.role == role:
        #         employees.append(employee)
        # return employees

    # def pay_employee(self, employee: Employee) -> None:
    #     """Pay an employee."""
    #     if isinstance(employee, SalariedEmployee):
    #         print(
    #             f"Paying employee {employee.name} a monthly salary of ${employee.monthly_salary}."
    #         )
    #     elif isinstance(employee, HourlyEmployee):
    #         print(
    #             f"Paying employee {employee.name} a hourly rate of \
    #             ${employee.hourly_rate} for {employee.amount} hours."
    #         )


def main() -> None:
    """Main function."""

    company = Company()

    company.add_employee(SalariedEmployee(name="Louis", role=Role.MANAGER))
    company.add_employee(HourlyEmployee(name="Brenda", role=Role.PRESIDENT))
    company.add_employee(HourlyEmployee(name="Tim", role=Role.INTERN))

    print(company.find_employee(Role.VICEPRESIDENT))
    print(company.find_employee(Role.MANAGER))
    print(company.find_employee(Role.INTERN))
    company.employees[0].pay()
    # company.pay_employee(company.employees[0])
    company.employees[0].take_a_holiday()
    # company.employees[0].take_a_holiday(False)


if __name__ == "__main__":
    main()
