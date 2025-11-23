class CustomerUpdateSchema:
    """
    Data for updating customer profile (admin use).
    """

    def __init__(
        self,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        license_number: str | None = None,
    ):
        self.name = name
        self.email = email
        self.phone = phone
        self.license_number = license_number
