
""" Command Design Pattern """
# represent commands and have control over when they're executed
# it's a behavioral pattern that provides a way to encapsulate all
# knowledge about performing a certain operation into a single object

from banking.bank import Bank
from banking.controller import BankController
from banking.commands import Deposit, Withdrawal, Transfer, Batch

def main() -> None:

    # create a bank
    bank = Bank()

    # create a bank controller
    controller = BankController()

    # create some accounts
    account1 = bank.create_account("Apple")
    account2 = bank.create_account("Google")
    account3 = bank.create_account("Microsoft")

    controller.execute(Deposit(account1, 100000))
    controller.execute(Deposit(account2, 100000))
    controller.execute(Deposit(account3, 100000))

    controller.execute(
        Batch(
            commands=[
                Deposit(account1, 100000),
                Transfer(from_account=account1, to_account=account3, amount=100000),
                Transfer(from_account=account3, to_account=account2, amount=100000)
            ]
        )
    )
    controller.undo()
    controller.undo()
    controller.redo()
    controller.redo()

    # transfer
    controller.execute(
        Transfer(from_account=account2, to_account=account1, amount=50000)
    )

    controller.execute(Withdrawal(account1, 150000))
    controller.undo()
    controller.redo()

    print(bank)


if __name__ == "__main__":
    main()
