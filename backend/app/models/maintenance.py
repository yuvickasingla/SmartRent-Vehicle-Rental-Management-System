from typing import Optional, Type, TypeVar
from datetime import datetime
from .base_model import BaseModel
from ..utils import MaintenanceStatus

M = TypeVar("M", bound="MaintenanceRecord")


class MaintenanceRecord(BaseModel):
    """
    Maintenance activity for a vehicle.
    """

    table_name = "maintenance_records"

    def __init__(
        self,
        id: Optional[int] = None,
        vehicle_id: int | None = None,
        description: str | None = None,
        cost: float = 0.0,
        status: str = MaintenanceStatus.SCHEDULED.value,
        scheduled_date: datetime | None = None,
        completed_date: datetime | None = None,
    ):
        super().__init__(id=id)
        self.vehicle_id = vehicle_id
        self.description = description
        self.cost = cost
        self.status = status
        self.scheduled_date = scheduled_date or datetime.utcnow()
        self.completed_date = completed_date

    def to_dict(self) -> dict:
        return {
            "vehicle_id": self.vehicle_id,
            "description": self.description,
            "cost": self.cost,
            "status": self.status,
            "scheduled_date": self.scheduled_date,
            "completed_date": self.completed_date,
        }

    @classmethod
    def from_row(cls: Type[M], row: dict) -> M:
        return cls(
            id=row.get("id"),
            vehicle_id=row.get("vehicle_id"),
            description=row.get("description"),
            cost=row.get("cost"),
            status=row.get("status"),
            scheduled_date=row.get("scheduled_date"),
            completed_date=row.get("completed_date"),
        )

    def start(self) -> None:
        self.status = MaintenanceStatus.IN_PROGRESS.value

    def complete(self, cost: float) -> None:
        self.status = MaintenanceStatus.COMPLETED.value
        self.cost = cost
        self.completed_date = datetime.utcnow()
