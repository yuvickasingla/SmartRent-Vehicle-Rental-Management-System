from typing import Optional, Type, TypeVar
from datetime import datetime
from .base_model import BaseModel
from ..utils import BookingStatus

B = TypeVar("B", bound="Booking")


class Booking(BaseModel):
    """
    Booking linking a customer, vehicle, and optionally a driver.
    """

    table_name = "bookings"

    def __init__(
        self,
        id: Optional[int] = None,
        customer_id: int | None = None,
        vehicle_id: int | None = None,
        driver_id: int | None = None,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        status: str = BookingStatus.PENDING.value,
        total_amount: float = 0.0,
    ):
        super().__init__(id=id)
        self.customer_id = customer_id
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.total_amount = total_amount

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "vehicle_id": self.vehicle_id,
            "driver_id": self.driver_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status,
            "total_amount": self.total_amount,
        }

    @classmethod
    def from_row(cls: Type[B], row: dict) -> B:
        return cls(
            id=row.get("id"),
            customer_id=row.get("customer_id"),
            vehicle_id=row.get("vehicle_id"),
            driver_id=row.get("driver_id"),
            start_date=row.get("start_date"),
            end_date=row.get("end_date"),
            status=row.get("status"),
            total_amount=row.get("total_amount"),
        )

    def duration_days(self) -> int:
        """
        Compute the number of days in the booking. Minimum 1 day.
        """
        if not self.start_date or not self.end_date:
            return 1
        days = (self.end_date.date() - self.start_date.date()).days
        return days if days > 0 else 1

    def confirm(self) -> None:
        self.status = BookingStatus.CONFIRMED.value

    def complete(self) -> None:
        self.status = BookingStatus.COMPLETED.value

    def cancel(self) -> None:
        self.status = BookingStatus.CANCELLED.value
