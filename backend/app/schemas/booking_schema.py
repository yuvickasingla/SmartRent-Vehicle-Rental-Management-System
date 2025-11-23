from datetime import datetime


class BookingCreateSchema:
    """
    Data for creating a booking from customer request.
    """

    def __init__(
        self,
        vehicle_id: int,
        start_date: str,
        end_date: str,
        driver_id: int | None = None,
    ):
        self.vehicle_id = vehicle_id
        self.driver_id = driver_id
        # Expect ISO format "YYYY-MM-DD"
        self.start_date = datetime.fromisoformat(start_date)
        self.end_date = datetime.fromisoformat(end_date)
