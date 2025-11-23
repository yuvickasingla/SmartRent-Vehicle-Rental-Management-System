from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class VehicleType(str, Enum):
    CAR = "car"
    BIKE = "bike"


class VehicleStatus(str, Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    UPI = "upi"


class MaintenanceStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
