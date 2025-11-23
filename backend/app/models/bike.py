from typing import Optional
from .vehicle import Vehicle
from ..utils import VehicleType


class Bike(Vehicle):
    """
    Bike is a specialization of Vehicle.

    Again, data is stored in the same 'vehicles' table,
    but we mark vehicle_type = 'bike' and use bike-specific fields.
    """

    def __init__(
        self,
        id: Optional[int] = None,
        registration_number: str | None = None,
        brand: str | None = None,
        model: str | None = None,
        daily_rate: float = 0.0,
        status: str | None = None,
        engine_cc: int = 110,
        has_gear: bool = True,
    ):
        super().__init__(
            id=id,
            registration_number=registration_number,
            brand=brand,
            model=model,
            daily_rate=daily_rate,
            vehicle_type=VehicleType.BIKE.value,
            status=status or VehicleType.BIKE.value,
            engine_cc=engine_cc,
            has_gear=has_gear,
        )
