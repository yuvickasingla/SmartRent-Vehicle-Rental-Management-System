from .vehicle_schema import VehicleCreateSchema
from.user_schema import UserLoginSchema, UserRegisterCustomerSchema
from .vehicle_schema import VehicleCreateSchema
from .customer_schema import CustomerUpdateSchema
from .booking_schema import BookingCreateSchema
from .driver_schema import DriverCreateSchema
from .payment_schema import PaymentCreateSchema
from .maintenance_schema import MaintenanceCreateSchema

__all__ = [
    "UserLoginSchema",
    "UserRegisterCustomerSchema",
    "VehicleCreateSchema",
    "CustomerUpdateSchema",
    "BookingCreateSchema",
    "DriverCreateSchema",
    "PaymentCreateSchema",
    "MaintenanceCreateSchema",
]
