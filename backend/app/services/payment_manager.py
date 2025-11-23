from typing import List, Optional
from .base_service import BaseService
from ..models import Payment, Booking
from ..schemas import PaymentCreateSchema
from ..utils import PaymentStatus


class PaymentManager(BaseService[Payment]):
    """
    Handles payment records for bookings.
    """

    def __init__(self):
        super().__init__(Payment)

    def create_payment(self, schema: PaymentCreateSchema) -> Payment:
        booking = Booking.get_by_id(schema.booking_id)
        if not booking:
            raise ValueError("Booking not found")

        payment = Payment(
            booking_id=booking.id,
            amount=schema.amount,
            method=schema.method,
            status=PaymentStatus.PENDING.value,
        ).save()

        return payment

    def mark_paid(self, payment_id: int, reference: str | None = None) -> Optional[Payment]:
        payment = self.get_by_id(payment_id)
        if not payment:
            return None

        payment.mark_paid(reference)
        payment.save()
        return payment

    def list_payments_by_customer(self, customer_id: int) -> List[Payment]:
        """
        List payments for all bookings of a customer.
        """
        all_payments = self.get_all()
        # Need bookings to know which belongs to customer
        result = []
        for p in all_payments:
            booking = Booking.get_by_id(p.booking_id)
            if booking and booking.customer_id == customer_id:
                result.append(p)
        return result
