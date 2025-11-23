class PaymentCreateSchema:
    def __init__(self, booking_id: int, amount: float, method: str):
        self.booking_id = booking_id
        self.amount = amount
        self.method = method
