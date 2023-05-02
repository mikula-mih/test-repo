
""" SOLID principles """
# stands for 5 principles:
# 1. [S]ingle Responsibility
# 2. [O]pen/Closed
# 3. [L]iskov Substitution
# 4. [I]nterface Segregation
# 5. [D]ependency Inversion

from abc import ABC, abstractmethod

class Order:
    items = []
    quantities = []
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass


class NotARobot(Authorizer):

    authorized = False

    def not_a_robot(self):
        print(f"Are you a robot? Naaa...")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class SMSAuth(Authorizer):

    authorized = False

    def verify_code(self, code):
        print(f"Verifying code {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized


class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, order):
        pass

class PaymentProcessor_SMS(PaymentProcessor):

    @abstractmethod
    def auth_sms(self, code):
        pass

class DebitPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code, authorizer: Authorizer):
        self.authorizer = authorizer
        self.security_code = security_code

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception("Not authorized")
        print("Ptocessing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentProcessor_SMS):

    def __init__(self, email_address):
        self.email_address = email_address
        self.verified = False

    def auth_sms(self, code):
        print(f'Verifying SMS code {code}')
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Verifying email address: {self.email_address}")
        order.status = "paid"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
authorizer = SMSAuth()
processor = PaypalPaymentProcessor("your@email.com")
processor.auth_sms("1234")
processor.pay(order)
processorDebit = DebitPaymentProcessor("2345678", authorizer)
authorizer.verify_code("1234")
processorDebit.pay(order)
