from typing import List, Optional
from .base_service import BaseService
from ..models import Vehicle
from ..schemas import VehicleCreateSchema
from ..utils import VehicleType, VehicleStatus


class VehicleManager(BaseService[Vehicle]):
    """
    Business logic for managing vehicles (admin).
    """

    def __init__(self):
        super().__init__(Vehicle)

    def create_vehicle(self, schema: VehicleCreateSchema) -> Vehicle:
        vtype = schema.vehicle_type.lower()

        if vtype not in (VehicleType.CAR.value, VehicleType.BIKE.value):
            raise ValueError("vehicle_type must be 'car' or 'bike'")

        vehicle = Vehicle(
            registration_number=schema.registration_number,
            brand=schema.brand,
            model=schema.model,
            daily_rate=schema.daily_rate,
            vehicle_type=vtype,
            status=VehicleStatus.AVAILABLE.value,
            seats=schema.seats,
            transmission=schema.transmission,
            engine_cc=schema.engine_cc,
            has_gear=schema.has_gear,
        ).save()

        return vehicle

    def update_vehicle(self, vehicle_id: int, data: dict) -> Optional[Vehicle]:
        vehicle = self.get_by_id(vehicle_id)
        if not vehicle:
            return None

        # Simple partial update: only update keys present in data
        for field in [
            "registration_number",
            "brand",
            "model",
            "daily_rate",
            "vehicle_type",
            "status",
            "seats",
            "transmission",
            "engine_cc",
            "has_gear",
        ]:
            if field in data:
                setattr(vehicle, field, data[field])

        vehicle.save()
        return vehicle

    def list_available(self) -> List[Vehicle]:
        """
        List only vehicles that are available for booking.
        """
        all_vehicles = self.get_all()
        return [v for v in all_vehicles if v.status == VehicleStatus.AVAILABLE.value]
