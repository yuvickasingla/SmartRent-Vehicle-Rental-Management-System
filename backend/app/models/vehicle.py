from typing import Optional, Type, TypeVar
from .base_model import BaseModel
from ..utils import VehicleType, VehicleStatus

V = TypeVar("V", bound="Vehicle")


class Vehicle(BaseModel):
    """
    Base vehicle model.

    We store cars and bikes in the same table, with a 'vehicle_type' column.
    Car and Bike subclasses will just give nicer OOP types.
    """

    table_name = "vehicles"

    def __init__(
        self,
        id: Optional[int] = None,
        registration_number: str | None = None,
        brand: str | None = None,
        model: str | None = None,
        daily_rate: float = 0.0,
        vehicle_type: str = VehicleType.CAR.value,
        status: str = VehicleStatus.AVAILABLE.value,
        seats: Optional[int] = None,
        transmission: Optional[str] = None,
        engine_cc: Optional[int] = None,
        has_gear: Optional[bool] = None,
    ):
        super().__init__(id=id)
        self.registration_number = registration_number
        self.brand = brand
        self.model = model
        self.daily_rate = daily_rate
        self.vehicle_type = vehicle_type
        self.status = status
        # Car-specific
        self.seats = seats
        self.transmission = transmission
        # Bike-specific
        self.engine_cc = engine_cc
        self.has_gear = has_gear

    def to_dict(self) -> dict:
        return {
            "registration_number": self.registration_number,
            "brand": self.brand,
            "model": self.model,
            "daily_rate": self.daily_rate,
            "vehicle_type": self.vehicle_type,
            "status": self.status,
            "seats": self.seats,
            "transmission": self.transmission,
            "engine_cc": self.engine_cc,
            "has_gear": self.has_gear,
        }

    @classmethod
    def from_row(cls: Type[V], row: dict) -> V:
        return cls(
            id=row.get("id"),
            registration_number=row.get("registration_number"),
            brand=row.get("brand"),
            model=row.get("model"),
            daily_rate=row.get("daily_rate"),
            vehicle_type=row.get("vehicle_type"),
            status=row.get("status"),
            seats=row.get("seats"),
            transmission=row.get("transmission"),
            engine_cc=row.get("engine_cc"),
            has_gear=row.get("has_gear"),
        )

    def is_available(self) -> bool:
        return self.status == VehicleStatus.AVAILABLE.value

    def mark_rented(self) -> None:
        self.status = VehicleStatus.RENTED.value

    def mark_available(self) -> None:
        self.status = VehicleStatus.AVAILABLE.value

    def mark_maintenance(self) -> None:
        self.status = VehicleStatus.MAINTENANCE.value
