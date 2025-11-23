from typing import Type, TypeVar, Generic, Optional, List
from ..models import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseService(Generic[T]):
    """
    Generic service class that wraps common CRUD operations
    around a given model class.
    """

    def __init__(self, model_cls: Type[T]):
        self.model_cls = model_cls

    def get_by_id(self, record_id: int) -> Optional[T]:
        return self.model_cls.get_by_id(record_id)

    def get_all(self) -> List[T]:
        return self.model_cls.get_all()

    def delete(self, record_id: int) -> bool:
        instance = self.get_by_id(record_id)
        if not instance:
            return False
        instance.delete()
        return True
