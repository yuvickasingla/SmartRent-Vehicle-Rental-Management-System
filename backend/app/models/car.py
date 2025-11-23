from typing import Optional
from .vehicle import Vehicle
from ..utils import VehicleType


class Car(Vehicle):
    """
    Car is a specialization of Vehicle in OOP terms.
    We still store everything in the 'vehicles' table.

    The constructor just pre-sets vehicle_type to 'car'
    and focuses on car-specific fields.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        registration_number: str | None = None,
        brand: str | None = None,
        model: str | None = None,
        daily_rate: float = 0.0,
        status: str | None = None,
        seats: int = 4,
        transmission: str = "manual",
    ):
        super().__init__(
            id=id,
            registration_number=registration_number,
            brand=brand,
            model=model,
            daily_rate=daily_rate,
            vehicle_type=VehicleType.CAR.value,
            status=status or VehicleType.CAR.value,  # fallback if needed
            seats=seats,
            transmission=transmission,
        )
