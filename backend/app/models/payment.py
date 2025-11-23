from typing import Optional, Type, TypeVar
from .base_model import BaseModel
from ..utils import PaymentStatus, PaymentMethod

P = TypeVar("P", bound="Payment")


class Payment(BaseModel):
    """
    Payment associated with a booking.
    """

    table_name = "payments"

    def __init__(
        self,
        id: Optional[int] = None,
        booking_id: int | None = None,
        amount: float = 0.0,
        status: str = PaymentStatus.PENDING.value,
        method: str = PaymentMethod.CASH.value,
        transaction_reference: str | None = None,
    ):
        super().__init__(id=id)
        self.booking_id = booking_id
        self.amount = amount
        self.status = status
        self.method = method
        self.transaction_reference = transaction_reference

    def to_dict(self) -> dict:
        return {
            "booking_id": self.booking_id,
            "amount": self.amount,
            "status": self.status,
            "method": self.method,
            "transaction_reference": self.transaction_reference,
        }

    @classmethod
    def from_row(cls: Type[P], row: dict) -> P:
        return cls(
            id=row.get("id"),
            booking_id=row.get("booking_id"),
            amount=row.get("amount"),
            status=row.get("status"),
            method=row.get("method"),
            transaction_reference=row.get("transaction_reference"),
        )

    def mark_paid(self, reference: str | None = None) -> None:
        self.status = PaymentStatus.PAID.value
        self.transaction_reference = reference

    def mark_failed(self) -> None:
        self.status = PaymentStatus.FAILED.value
