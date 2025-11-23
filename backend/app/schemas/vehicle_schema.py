class VehicleCreateSchema:
    """
    Data needed to create a vehicle (car or bike).
    """

    def __init__(
        self,
        registration_number: str,
        brand: str,
        model: str,
        daily_rate: float,
        vehicle_type: str,
        seats: int | None = None,
        transmission: str | None = None,
        engine_cc: int | None = None,
        has_gear: bool | None = None,
    ):
        self.registration_number = registration_number
        self.brand = brand
        self.model = model
        self.daily_rate = daily_rate
        self.vehicle_type = vehicle_type
        self.seats = seats
        self.transmission = transmission
        self.engine_cc = engine_cc
        self.has_gear = has_gear
