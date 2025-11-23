from typing import List, Optional
from .base_service import BaseService
from ..models import MaintenanceRecord, Vehicle
from ..schemas import MaintenanceCreateSchema


class MaintenanceManager(BaseService[MaintenanceRecord]):
    """
    Admin logic for vehicle maintenance.
    """

    def __init__(self):
        super().__init__(MaintenanceRecord)

    def create_record(self, schema: MaintenanceCreateSchema) -> MaintenanceRecord:
        vehicle = Vehicle.get_by_id(schema.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        vehicle.mark_maintenance()
        vehicle.save()

        record = MaintenanceRecord(
            vehicle_id=vehicle.id,
            description=schema.description,
        ).save()

        return record

    def complete_record(self, record_id: int, cost: float) -> Optional[MaintenanceRecord]:
        record = self.get_by_id(record_id)
        if not record:
            return None

        record.complete(cost)
        record.save()

        vehicle = Vehicle.get_by_id(record.vehicle_id)
        if vehicle:
            vehicle.mark_available()
            vehicle.save()

        return record
