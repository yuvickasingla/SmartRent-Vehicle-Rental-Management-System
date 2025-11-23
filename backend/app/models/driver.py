from typing import Optional, Type, TypeVar
from .base_model import BaseModel
from ..utils import validate_phone
from ..database import db

D = TypeVar("D", bound="Driver")


class Driver(BaseModel):
    """
    Driver that can be assigned to bookings.
    """

    table_name = "drivers"

    def __init__(
        self,
        id: Optional[int] = None,
        name: str | None = None,
        phone: str | None = None,
        license_number: str | None = None,
        is_available: bool = True,
    ):
        super().__init__(id=id)
        self.name = name
        self.phone = phone
        self.license_number = license_number
        self.is_available = is_available

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "phone": self.phone,
            "license_number": self.license_number,
            "is_available": self.is_available,
        }

    @classmethod
    def from_row(cls: Type[D], row: dict) -> D:
        return cls(
            id=row.get("id"),
            name=row.get("name"),
            phone=row.get("phone"),
            license_number=row.get("license_number"),
            is_available=row.get("is_available") == 1
            if isinstance(row.get("is_available"), int)
            else row.get("is_available"),
        )

    def validate(self) -> None:
        if self.phone:
            validate_phone(self.phone)

    def save(self):
        self.validate()
        return super().save()

    def assign(self) -> None:
        self.is_available = False

    def release(self) -> None:
        self.is_available = True

    @classmethod
    def get_available_drivers(cls: Type[D]) -> list[D]:
        sql = f"SELECT * FROM {cls.table_name} WHERE is_available = 1"
        rows = db.query_all(sql)
        return [cls.from_row(row) for row in rows]
