from typing import Optional, Type, TypeVar
from .base_model import BaseModel
from ..database import db
from ..utils import UserRole

U = TypeVar("U", bound="User")


class User(BaseModel):
    """
    User model represents both admin and customer logins.

    Columns:
      id, username, password, role ('admin' or 'customer'), customer_id (FK)

    For admin users, customer_id will be NULL.
    For customer users, customer_id links to a Customer record.
    """

    table_name = "users"

    def __init__(
        self,
        id: Optional[int] = None,
        username: str | None = None,
        password: str | None = None,
        role: str = UserRole.CUSTOMER.value,
        customer_id: Optional[int] = None,
    ):
        super().__init__(id=id)
        self.username = username
        self.password = password  # plain text per your requirement
        self.role = role
        self.customer_id = customer_id

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "customer_id": self.customer_id,
        }

    @classmethod
    def from_row(cls: Type[U], row: dict) -> U:
        return cls(
            id=row.get("id"),
            username=row.get("username"),
            password=row.get("password"),
            role=row.get("role"),
            customer_id=row.get("customer_id"),
        )

    @classmethod
    def find_by_username(cls: Type[U], username: str) -> Optional[U]:
        sql = f"SELECT * FROM {cls.table_name} WHERE username = %s"
        row = db.query_one(sql, [username])
        if row is None:
            return None
        return cls.from_row(row)
