from typing import List, Optional
from .base_service import BaseService
from ..models import Booking, Vehicle, Driver
from ..schemas import BookingCreateSchema
from ..utils import BookingStatus


class RentalManager(BaseService[Booking]):
    """
    Handles booking creation and lifecycle.
    """

    def __init__(self):
        super().__init__(Booking)

    def create_booking(self, customer_id: int, schema: BookingCreateSchema) -> Booking:
        """
        Create a booking for the given customer with selected vehicle and driver.
        """
        vehicle = Vehicle.get_by_id(schema.vehicle_id)
        if not vehicle:
            raise ValueError("Vehicle not found")

        if not vehicle.is_available():
            raise ValueError("Vehicle is not available")

        driver = None
        if schema.driver_id is not None:
            driver = Driver.get_by_id(schema.driver_id)
            if not driver:
                raise ValueError("Driver not found")
            if not driver.is_available:
                raise ValueError("Driver not available")

        booking = Booking(
            customer_id=customer_id,
            vehicle_id=vehicle.id,
            driver_id=driver.id if driver else None,
            start_date=schema.start_date,
            end_date=schema.end_date,
            status=BookingStatus.PENDING.value,
        )

        # Pricing: daily_rate * number of days
        booking.total_amount = booking.duration_days() * vehicle.daily_rate
        booking.save()

        # update vehicle and driver statuses
        vehicle.mark_rented()
        vehicle.save()

        if driver:
            driver.assign()
            driver.save()

        return booking

    def complete_booking(self, booking_id: int) -> Optional[Booking]:
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        booking.complete()
        booking.save()

        vehicle = Vehicle.get_by_id(booking.vehicle_id)
        if vehicle:
            vehicle.mark_available()
            vehicle.save()

        if booking.driver_id:
            driver = Driver.get_by_id(booking.driver_id)
            if driver:
                driver.release()
                driver.save()

        return booking

    def cancel_booking(self, booking_id: int) -> Optional[Booking]:
        booking = self.get_by_id(booking_id)
        if not booking:
            return None

        booking.cancel()
        booking.save()

        vehicle = Vehicle.get_by_id(booking.vehicle_id)
        if vehicle:
            vehicle.mark_available()
            vehicle.save()

        if booking.driver_id:
            driver = Driver.get_by_id(booking.driver_id)
            if driver:
                driver.release()
                driver.save()

        return booking

    def list_bookings_by_customer(self, customer_id: int) -> List[Booking]:
        all_bookings = self.get_all()
        return [b for b in all_bookings if b.customer_id == customer_id]
