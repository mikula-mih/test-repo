class PaymentHandler(Protocol):
    def handle_payment(self, amount: int) -> None:
        ...

class StripePaymentHandler:
    def handle_payment(self, amount: int) -> None:
        print(f"Charging ${amount/100:.2f} using Stripe")

class PayPalPaymentHandler:
    def handle_payment(self, amount: int) -> None:
        print(f"Charging ${amount/100:.2f} using PayPal")

PRICES = {
    "burger": 10_00,
    "fries": 5_00,
    "drink": 2_00,
    "salad": 15_00,
}


def order_food(items: list[str], payment_handler: PaymentHandler) -> None: # dependency inversion
    total = sum(PRICES[item] for item in items)
    print(f"Your order is ${total/100:.2f}.")
    payment_handler.handle_payment(total)
    print(f"Thanks for your business!")

def main() -> None:
    order_food(["burger", "salad", "drink"], PayPalPaymentHandler()) # dependency injection

if __name__ == "__main__":
    main()
