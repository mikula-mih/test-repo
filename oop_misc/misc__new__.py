from enum import Enum
from typing import Protocol


# no need to do this in such a complicated way
class Payment:
    def __new__(cls, payment_type: str):
        if payment_type == "paypal":
            return object.__new__(PaypalPayment)
        elif payment_type == "card":
            return object.__new__(StripePayment)

    def pay(self, amount: int) -> None:
        raise NotImplementedError

# Better use `Factory method pattern`
class PaymentMethod(Enum):
    PAYPAL = "paypal"
    CARD = "card"

class Payment(Protocol):
    def pay(self, amount: int) -> None:
        ...

class PaypalPayment(Payment):
    def pay(self, amount: int) -> None:
        print(f"Paying {amount} using Paypal")

class StripePayment(Payment):
    def pay(self, amount: int) -> None:
        print(f"Paying {amount} using Stripe")

PAYMENT_METHODS: dict[PaymentMethod, type[Payment]] = {
    PaymentMethod.CARD: StripePayment,
    PaymentMethod.PAYPAL: PaypalPayment,
}

def main_not_the_best() -> None:
    # it's realy a StripePayment()
    my_payment = Payment("card")
    if my_payment:
        my_payment.pay(100)

def main():
    my_payment = PAYMENT_METHODS[PaymentMethod.PAYPAL]()
    my_payment.pay(100)




if __name__ == "__main__":
    # main_not_the_best()
    main()
