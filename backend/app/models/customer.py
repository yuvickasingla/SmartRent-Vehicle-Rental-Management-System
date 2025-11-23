from typing import Optional, Type, TypeVar
from .base_model import BaseModel
from ..utils import validate_email, validate_phone, ValidationError
from ..database import db

C = TypeVar("C", bound="Customer")


class Customer(BaseModel):
    """
    Customer profile information.

    Separate from User so that we can store more details here.
    """

    table_name = "customers"

    def __init__(
        self,
        id: Optional[int] = None,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        license_number: str | None = None,
    ):
        super().__init__(id=id)
        self.name = name
        self.email = email
        self.phone = phone
        self.license_number = license_number

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "license_number": self.license_number,
        }

    @classmethod
    def from_row(cls: Type[C], row: dict) -> C:
        return cls(
            id=row.get("id"),
            name=row.get("name"),
            email=row.get("email"),
            phone=row.get("phone"),
            license_number=row.get("license_number"),
        )

    def validate(self) -> None:
        """
        Run basic validation on email and phone.
        """
        if self.email:
            validate_email(self.email)
        if self.phone:
            validate_phone(self.phone)

    def save(self):
        """
        Override save to add validation before writing to DB.
        """
        self.validate()
        return super().save()

    @classmethod
    def find_by_email(cls: Type[C], email: str) -> Optional[C]:
        sql = f"SELECT * FROM {cls.table_name} WHERE email = %s"
        row = db.query_one(sql, [email])
        if row is None:
            return None
        return cls.from_row(row)
