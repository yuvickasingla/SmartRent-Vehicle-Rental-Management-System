from abc import ABC, abstractmethod
from typing import List, Type, TypeVar, Optional
from ..database import db

T = TypeVar("T", bound="BaseModel")


class BaseModel(ABC):
    """
    Base class for all models.

    Each subclass must define:
      - table_name (str)
      - to_dict()  -> dict of column values (excluding 'id')
      - from_row() -> classmethod to create an object from DB row dict

    This class provides save(), delete(), get_by_id(), get_all()
    using mysql-connector through the shared 'db' object.
    """

    table_name: str = ""

    def __init__(self, id: Optional[int] = None):
        self.id = id

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Must return a dict of column_name -> value, excluding 'id'.
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_row(cls: Type[T], row: dict) -> T:
        """
        Must construct an instance of the subclass from a DB row dict.
        """
        raise NotImplementedError

    def save(self: T) -> T:
        """
        Insert or update the record depending on whether id is set.
        """
        data = self.to_dict()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = list(data.values())

        if self.id is None:
            # INSERT
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            new_id = db.execute(sql, values)
            self.id = new_id
        else:
            # UPDATE
            set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE id = %s"
            values.append(self.id)
            db.execute(sql, values)
        return self

    def delete(self) -> None:
        """
        Delete this record from the database if it has an id.
        """
        if self.id is None:
            return
        sql = f"DELETE FROM {self.table_name} WHERE id = %s"
        db.execute(sql, [self.id])
        self.id = None

    @classmethod
    def get_by_id(cls: Type[T], record_id: int) -> Optional[T]:
        sql = f"SELECT * FROM {cls.table_name} WHERE id = %s"
        row = db.query_one(sql, [record_id])
        if row is None:
            return None
        return cls.from_row(row)

    @classmethod
    def get_all(cls: Type[T]) -> List[T]:
        sql = f"SELECT * FROM {cls.table_name}"
        rows = db.query_all(sql)
        return [cls.from_row(row) for row in rows]
