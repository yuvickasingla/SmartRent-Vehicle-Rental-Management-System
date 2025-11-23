from typing import List, Optional
from .base_service import BaseService
from ..models import Driver
from ..schemas import DriverCreateSchema


class DriverManager(BaseService[Driver]):
    """
    Admin logic for managing drivers.
    """

    def __init__(self):
        super().__init__(Driver)

    def create_driver(self, schema: DriverCreateSchema) -> Driver:
        driver = Driver(
            name=schema.name,
            phone=schema.phone,
            license_number=schema.license_number,
            is_available=True,
        ).save()
        return driver

    def list_available(self) -> List[Driver]:
        return Driver.get_available_drivers()

    def update_driver(self, driver_id: int, data: dict) -> Optional[Driver]:
        driver = self.get_by_id(driver_id)
        if not driver:
            return None

        for field in ["name", "phone", "license_number", "is_available"]:
            if field in data:
                setattr(driver, field, data[field])

        driver.save()
        return driver
